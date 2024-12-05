import os

import inject
from textual.widgets import RichLog
import redis.asyncio as redis

from .protocols.executor import ExecutorProtocol
from .protocols.path import PathProtocol
from .protocols.pipelines import PipelinesProtocol, PipelineStorageProtocol
from .protocols.ui_log import UILogProtocol
from .services.local_path import LocalPath
from .services.pypyr_pipelines import PypyrPipelines
from .services.redis_executor import RedisExecutor
from .services.redis_pipeline_storage import RedisPipelineStorage
from .services.rich_ui_log import RichUILogService


def default_config(binder: inject.Binder):
    pool = redis.ConnectionPool.from_url(os.environ['NOSTROMO_REDIS_URL'])
    client = redis.Redis.from_pool(pool)
    binder.bind_to_constructor(PathProtocol, lambda: LocalPath())
    binder.bind_to_constructor(PipelineStorageProtocol, lambda: RedisPipelineStorage(client))
    binder.bind_to_constructor(ExecutorProtocol, lambda: RedisExecutor(os.environ['NOSTROMO_REDIS_URL']))


def ui_config(binder: inject.Binder):
    binder.install(default_config)

    pool = redis.ConnectionPool.from_url(os.environ['NOSTROMO_REDIS_URL'])
    client = redis.Redis.from_pool(pool)

    binder.bind_to_constructor(PipelinesProtocol, lambda: PypyrPipelines(client))
    binder.bind_to_constructor(UILogProtocol, lambda: RichUILogService(RichLog(highlight=True, markup=True)))
