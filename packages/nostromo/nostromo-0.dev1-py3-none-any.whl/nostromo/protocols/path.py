import abc
from pathlib import Path
from typing import Protocol


class PathProtocol(Protocol, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def root(self) -> Path:
        pass

    @property
    @abc.abstractmethod
    def scripts(self) -> Path:
        pass

    @property
    @abc.abstractmethod
    def env_file(self) -> Path:
        pass

    @property
    @abc.abstractmethod
    def storage(self) -> Path:
        pass

    @property
    @abc.abstractmethod
    def pipelines(self) -> Path:
        pass

    @property
    @abc.abstractmethod
    def logs(self) -> Path:
        pass

    @property
    @abc.abstractmethod
    def pipelines_logs(self) -> Path:
        pass

    @property
    @abc.abstractmethod
    def scheduler_logs(self) -> Path:
        pass

    @abc.abstractmethod
    def ensure_log_dirs(self):
        pass
