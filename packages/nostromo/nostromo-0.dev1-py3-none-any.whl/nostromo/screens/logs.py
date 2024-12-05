import inject
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer

from ..protocols.ui_log import UILogProtocol


class LogsScreen(Screen):
    _log: UILogProtocol = inject.attr(UILogProtocol)
    BINDINGS = [('ctrl+l', 'app.pop_screen', 'Close Logs')]

    def compose(self) -> ComposeResult:
        yield self._log.log
        yield Footer()
