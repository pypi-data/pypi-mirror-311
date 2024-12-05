from os import environ, makedirs
from pathlib import PosixPath

import func_timeout
import inject
import typer
from func_timeout import FunctionTimedOut
from redis import Redis

from .app import Nostromo
from .injector import ui_config


class Runner:
    def _check_redis(self):
        if not environ.get('NOSTROMO_REDIS_URL'):
            environ['NOSTROMO_REDIS_URL'] = 'redis://localhost'

        Redis.from_url(environ['NOSTROMO_REDIS_URL']).ping()

    def _validate(self):
        if not environ.get('NOSTROMO_HOME'):
            environ['NOSTROMO_HOME'] = '~/.nostromo'

        full_path = PosixPath(environ['NOSTROMO_HOME']).expanduser()
        makedirs(full_path, exist_ok=True)

        try:
            func_timeout.func_timeout(2, self._check_redis, )
        except FunctionTimedOut:
            print(f'Redis connection error. Check connection or modify NOSTROMO_REDIS_URL variable')
            exit(1)

    def run_ui(self):
        self._validate()
        inject.configure(ui_config)
        Nostromo().run(mouse=False)

    def run_scheduler(self):
        self._validate()


app = typer.Typer(
    help='Default env variables: NOSTROMO_HOME=~/.nostromo, NOSTROMO_REDIS_URL=redis://localhost',
    add_completion=False,
)


@app.command(help='open terminal')
def ui():
    Runner().run_ui()


@app.command(help='run scheduler')
def scheduler():
    Runner().run_scheduler()


if __name__ == "__main__":
    app()
