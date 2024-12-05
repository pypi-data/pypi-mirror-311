import abc
from typing import Protocol

from ..models.pipeline import Pipeline


class PipelineEditorProtocol(Protocol, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_pipeline(self, pipeline: str) -> Pipeline:
        pass
