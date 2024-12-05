import abc
from typing import Protocol, List, Dict

from ..models.pipeline import Pipeline, PipelineTask, PipelineTaskGroup, PipelineRun


class PipelinesProtocol(Protocol, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def entrypoints(self) -> List[str]:
        pass

    @abc.abstractmethod
    def get_scripts_by_entrypoint(self, entrypoint: str) -> List[str]:
        pass

    @abc.abstractmethod
    def get_nostromo_env(self) -> Dict[str, str]:
        pass

    @abc.abstractmethod
    def get_task_names(self, pipeline: Pipeline) -> List[str]:
        pass

    @abc.abstractmethod
    def get_group_names(self, pipeline: Pipeline) -> List[str]:
        pass

    @abc.abstractmethod
    def add_task_to_group(self, group_name: str, task: PipelineTask) -> PipelineTaskGroup:
        pass

    def get_pipelines(self) -> List[Pipeline]:
        pass

    async def run_pipeline_by_name(self, name: str) -> PipelineRun:
        pass

    def get_pipeline_by_name(self, name: str) -> Pipeline:
        pass

    async def get_last_pipeline_run(self, pipeline_name: str) -> PipelineRun:
        pass

    async def kill_pipeline(self, run: PipelineRun) -> PipelineRun:
        pass


class PipelineStorageProtocol(Protocol, metaclass=abc.ABCMeta):
    async def get_pipelines(self) -> List[Pipeline]:
        pass
