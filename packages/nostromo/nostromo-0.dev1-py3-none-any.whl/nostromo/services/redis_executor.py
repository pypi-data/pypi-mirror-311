from redis.asyncio import Redis
from saq import Queue

from ..protocols.executor import ExecutorProtocol


class RedisExecutor(ExecutorProtocol):
    def __init__(self, redis_url: str):
        self._queue = Queue.from_url(redis_url)
        self._client = Redis.from_url(redis_url)

    async def send_to_executor(self, cmd: str):
        return await super().send_to_executor(cmd)

    async def wait_and_exec_commands(self):
        return await super().wait_and_exec_commands()

    async def is_scheduler_running(self) -> bool:
        return await super().is_scheduler_running()

    async def set_scheduler_running(self, is_scheduler_running: bool) -> None:
        return await super().set_scheduler_running(is_scheduler_running)

    async def action_pause_pipeline(self):
        pass

    async def action_kill_pipeline(self):
        pass

    async def wait_and_exec_actions(self):
        pass
