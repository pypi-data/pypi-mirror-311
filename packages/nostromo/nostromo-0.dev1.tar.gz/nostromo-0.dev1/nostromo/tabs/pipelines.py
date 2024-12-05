from asyncio import sleep

import inject
from rich.text import Text
from textual import work
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable

from ..protocols.pipelines import PipelinesProtocol
from ..protocols.ui_log import UILogProtocol


class _PipelinesTable(DataTable):
    DEFAULT_CSS = """
    _PipelinesTable {color: #c7c9ca; border-bottom: #1047A9; padding-bottom: 1} # FFBC40
    _PipelinesTable > .datatable--cursor {background: #1047A9; color: #c7c9ca}
    _PipelinesTable > .datatable--fixed-cursor {background: #1e1e1e; color: #c7c9ca}
    _PipelinesTable > .datatable--fixed {background: #1e1e1e; color: #c7c9ca}
    _PipelinesTable > .datatable--hover {background: #1e1e1e; color: #c7c9ca}
    _PipelinesTable > .datatable--header {background: #1e1e1e; color: #FFBC40}
    """
    _log = inject.attr(UILogProtocol)
    _pipelines = inject.attr(PipelinesProtocol)
    BINDINGS = [
        ('ctrl+r', 'run_pipeline()', 'Run Pipeline'),
        ('ctrl+k', 'kill_pipeline()', 'Kill Pipeline'),
        ('ctrl+p', 'stop_pipeline()', 'Pause Pipeline'),
    ]

    def action_run_pipeline(self):
        self._run_pipeline_by_name()

    @work(exclusive=True)
    async def _run_pipeline_by_name(self):
        pipeline_name = self.get_cell_at(self.cursor_coordinate)
        self.refresh_bindings()
        await self._pipelines.run_pipeline_by_name(pipeline_name)
        self._log.info(pipeline_name, 'Pipeline started')

    def action_kill_pipeline(self):
        self._kill_pipeline()

    @work(exclusive=True)
    async def _kill_pipeline(self):
        pipeline_name = self.get_cell_at(self.cursor_coordinate)
        self._log.warning(f'Kill pipeline {pipeline_name}')
        last_run = await self._pipelines.get_last_pipeline_run(pipeline_name)
        if not last_run or last_run.finished_at:
            self._log.error(f'{pipeline_name} is not running', 'Kill Error')
            return

        await self._pipelines.kill_pipeline(last_run)
        self._log.warning(pipeline_name, 'Pipeline killed')

    @work(exclusive=True)
    async def track_pipelines(self):
        while True:
            for row in self.rows.values():
                last_run = await self._pipelines.get_last_pipeline_run(row.key.value)
                if not last_run:
                    continue

                finished = last_run.finished_at.strftime('%Y-%m-%d %H:%M:%S') if last_run.finished_at else ''
                self.update_cell(row.key, 'Last Run', last_run.started_at.strftime('%Y-%m-%d %H:%M:%S'))
                self.update_cell(row.key, 'Duration', str(last_run.duration).split('.')[0])
                self.update_cell(row.key, 'Finished', finished)

            await sleep(1)


class PipelienesContent(Widget):
    _pipelines = inject.attr(PipelinesProtocol)

    @classmethod
    def get_id(cls):
        return 'Pipelines'

    def compose(self) -> ComposeResult:
        table = _PipelinesTable()
        table.cursor_type = 'row'
        table.zebra_stripes = True
        padding = ' ' * 20

        for col in (
            'Name',
            'Schedule',
            'Last Run',
            'Duration',
            'Finished',
        ):
            table.add_column(Text(col, justify='center'), key=col)

        for pipeline in self._pipelines.get_pipelines():
            table.add_row(
                pipeline.name,
                pipeline.schedule,
                padding,
                '',
                padding,
                key=pipeline.name,
            )

        table.sort('Name')
        yield table
