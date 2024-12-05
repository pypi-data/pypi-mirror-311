from asyncio import sleep
from typing import List
from redis.asyncio import Redis
from ..models.pipeline import Pipeline
from ..protocols.pipelines import PipelineStorageProtocol


class RedisPipelineStorage(PipelineStorageProtocol):
    def __init__(self, client: Redis):
        self._redis = client
        self._lock = self._redis.lock('/test', timeout=21, blocking_timeout=4)

    @property
    def pipelines_redis_key(self) -> str:
        return '/nostromo/pipelines/'

    def _get_redis_key_by_name(self, name: str) -> str:
        return f'{self.pipelines_redis_key}{name}'

    async def get_pipelines(self) -> List[Pipeline]:
        data = await self._redis.keys(self.pipelines_redis_key + '*')
        return data
