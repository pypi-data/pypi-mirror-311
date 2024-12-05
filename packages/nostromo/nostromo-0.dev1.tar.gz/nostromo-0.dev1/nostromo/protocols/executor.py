from abc import ABCMeta, abstractmethod
from typing import Protocol


class ExecutorProtocol(Protocol, metaclass=ABCMeta):
    @abstractmethod
    async def is_scheduler_running(self) -> bool:
        pass

    @abstractmethod
    async def set_scheduler_running(self, is_scheduler_running: bool) -> None:
        pass

    @abstractmethod
    async def send_to_executor(self, cmd: str):
        pass

    @abstractmethod
    async def wait_and_exec_commands(self):
        pass

    @abstractmethod
    async def action_pause_pipeline(self):
        pass

    @abstractmethod
    async def action_kill_pipeline(self):
        pass

    @abstractmethod
    async def wait_and_exec_actions(self):
        pass
