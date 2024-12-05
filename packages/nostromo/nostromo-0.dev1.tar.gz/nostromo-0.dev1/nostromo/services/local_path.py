import abc
import os
from pathlib import Path, PosixPath

from ..protocols.path import PathProtocol


class LocalPath(PathProtocol, metaclass=abc.ABCMeta):
    def __init__(self):
        nostromo_path = os.environ.get('NOSTROMO_HOME')
        if not nostromo_path:
            nostromo_path = '~/.nostromo'

        self._root = PosixPath(nostromo_path).expanduser()

        self._scripts = PosixPath(os.path.join(str(self._root), 'scripts'))
        self._storage = PosixPath(os.path.join(str(self._root), '.storage'))
        self._env_file = PosixPath(os.path.join(str(self._storage), 'env.yml'))
        self._pipelines = PosixPath(os.path.join(str(self._storage), 'pipelines'))

        self._logs = PosixPath(os.path.join(str(self._storage), 'logs'))
        self._pipelines_logs = PosixPath(os.path.join(str(self._logs), 'pipelines'))
        self._scheduler_logs = PosixPath(os.path.join(str(self._logs), 'scheduler'))

    @property
    def root(self) -> Path:
        return self._root

    @property
    def scripts(self) -> Path:
        return self._scripts

    @property
    def env_file(self) -> Path:
        return self._env_file

    @property
    def storage(self) -> Path:
        return self._storage

    @property
    def pipelines(self) -> Path:
        return self._pipelines

    @property
    def logs(self) -> Path:
        return self._logs

    @property
    def pipelines_logs(self) -> Path:
        return self._pipelines_logs

    @property
    def scheduler_logs(self) -> Path:
        return self._scheduler_logs

    def ensure_log_dirs(self):
        for dir_path in (
            self.logs,
            self.pipelines_logs,
            self.scheduler_logs,
        ):
            os.makedirs(dir_path, exist_ok=True)
