import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
from typing import List, Union


@dataclass
class PipelineTaskGroup:
    name: str
    children: List[Union['PipelineTask']] = field(default_factory=list)


@dataclass
class PipelineTask:
    name: str
    children: List[Union['PipelineTaskGroup', 'PipelineTask']] = field(default_factory=list)


class PipelineRunStatus:
    KILLED = 'killed'
    RUNNING = 'running'


@dataclass
class Pipeline:
    name: str
    pipeline_dir: str = ''
    schedule: str = ''


@dataclass
class PipelineRun:
    pipeline_name: str
    logs_dir: str
    started_at: datetime
    finished_at: Union[datetime, str] = ''
    pid: int = 0
    status: str = PipelineRunStatus.RUNNING

    @property
    def duration(self) -> timedelta:
        if self.finished_at:
            return self.finished_at - self.started_at
        return datetime.now(UTC) - self.started_at

    def to_json(self) -> str:
        data = self.__dict__
        for key in ('started_at', 'finished_at'):
            value = getattr(self, key)
            if value:
                data[key] = value.isoformat()
        return json.dumps(data)
