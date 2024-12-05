import codecs
import json
import os
import subprocess
from datetime import datetime, UTC
from typing import List, Dict

import inject
import psutil
import yaml
from psutil import NoSuchProcess
from redis.asyncio import Redis

from ..models.pipeline import Pipeline, PipelineTask, PipelineTaskGroup, PipelineRun, PipelineRunStatus
from ..protocols.path import PathProtocol
from ..protocols.pipelines import PipelinesProtocol


class PypyrPipelines(PipelinesProtocol):
    _paths = inject.attr(PathProtocol)

    def __init__(self, redis: Redis):
        self._redis = redis

    @property
    def logs_dt_format(self) -> str:
        return '%Y-%m-%d-%H_%M_%S'

    @property
    def entrypoints(self) -> List[str]:
        entrypoints = []
        for entrypoint in (
            'sh',
            'pyenv',
            'docker',
        ):
            try:
                subprocess.check_output(['which', entrypoint])
                entrypoints.append(entrypoint)
            except subprocess.CalledProcessError:
                continue

        return entrypoints

    def get_task_names(self, pipeline: Pipeline) -> List[str]:
        pass

    def get_group_names(self, pipeline: Pipeline) -> List[str]:
        pass

    def add_task_to_group(self, group_name: str, task: PipelineTask) -> PipelineTaskGroup:
        pass

    def get_scripts_by_entrypoint(self, entrypoint: str) -> List[str]:
        result = []
        if entrypoint == 'docker':
            images = subprocess.check_output(['docker', 'images', '--format=json'])
            images = images.decode().split('\n')

            for image_str in images:
                if not image_str:
                    continue

                image = json.loads(image_str)
                result.append(f'{image["Repository"]}:{image["Tag"]}')
        else:
            endswith = '.py' if entrypoint in ('pyenv', ) else '.sh'
            for file in os.scandir(self._paths.scripts):
                if file.name.endswith(endswith):
                    result.append(file.name)

        return sorted(result)

    def get_nostromo_env(self) -> Dict[str, str]:
        config = {}
        config['NOSTOMO_HOME'] = os.environ.get('NOSTOMO_HOME')
        return dict(sorted(config.items(), key=lambda x: x[0]))

    def _load_pipeline_from_yml(self, folder_name: str) -> Pipeline:
        full_dir = os.path.join(self._paths.pipelines, folder_name)
        with codecs.open(os.path.join(full_dir, '.pipeline.yaml')) as stream:
            params = yaml.safe_load(stream) or {}
            params['pipeline_dir'] = full_dir
            params['name'] = folder_name
            return Pipeline(**params)

    def get_pipelines(self) -> List[Pipeline]:
        return []
        return [
            self._load_pipeline_from_yml(p)
            for p in os.listdir(self._paths.pipelines)
        ]

    def _get_pipeline_logs_dir(self, name: str) -> str:
        return os.path.join(str(self._paths.pipelines_logs), name)

    async def get_last_pipeline_run(self, pipeline_name: str) -> PipelineRun or None:
        pattern = self._get_pipeline_runs_key(pipeline_name) + '*'
        keys = await self._redis.scan(match=pattern.encode(), count=1)
        if not keys[1]:
            return

        run_key = keys[1][0].decode()
        data = await self._redis.get(run_key)
        if not data:
            return

        record: dict = json.loads(data.decode('utf-8'))
        for key in ('started_at', 'finished_at'):
            if record.get(key):
                record[key] = datetime.fromisoformat(record[key])

        return PipelineRun(**record)

    async def kill_pipeline(self, run: PipelineRun) -> PipelineRun:
        try:
            parent = psutil.Process(run.pid)
        except NoSuchProcess:
            run.status = PipelineRunStatus.KILLED
            run.finished_at = datetime.now(UTC)
            await self._save_pipeline_run(run)
            return run

        for child in parent.children(recursive=True):
            try:
                child.kill()
            except NoSuchProcess:
                pass

        parent.kill()
        run.status = PipelineRunStatus.KILLED
        run.finished_at = datetime.now(UTC)
        await self._save_pipeline_run(run)

    def _get_pipeline_runs_key(self, pipeline_name: str) -> str:
        return f'nostromo:pipeline_run:{pipeline_name}'

    async def _save_pipeline_run(self, run: PipelineRun) -> None:
        key = self._get_pipeline_runs_key(pipeline_name=run.pipeline_name)
        run_dt = run.started_at.strftime(self.logs_dt_format)
        key = f'{key}:{run_dt}'

        await self._redis.set(key, run.to_json())

    def get_pipeline_by_name(self, name: str) -> Pipeline:
        return self._load_pipeline_from_yml(name)

    async def run_pipeline_by_name(self, name: str) -> PipelineRun:
        pipeline = self.get_pipeline_by_name(name)
        pypyr_path = subprocess.check_output(
            'which pypyr',
            shell=True,
            env=os.environ,
            text=True
        ).replace('\n', '')

        run = datetime.now(UTC)
        logs_dir = os.path.join(self._get_pipeline_logs_dir(name), run.strftime(self.logs_dt_format))

        os.makedirs(logs_dir, exist_ok=True)
        process = subprocess.Popen(
            f'{pypyr_path} .run pipeline_log_dir={logs_dir}',
            shell=True,
            text=True,
            cwd=pipeline.pipeline_dir,
        )

        pipeline_run = PipelineRun(
            pid=process.pid,
            logs_dir=logs_dir,
            pipeline_name=pipeline.name,
            started_at=run,
        )

        await self._save_pipeline_run(pipeline_run)
        return pipeline_run
