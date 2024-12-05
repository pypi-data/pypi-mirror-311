from datetime import datetime, UTC

from textual.notifications import SeverityLevel
from textual.widgets import RichLog

from ..protocols.ui_log import UILogProtocol


class RichUILogService(UILogProtocol):
    def __init__(self, log: RichLog):
        self._log = log

    @property
    def log(self) -> RichLog:
        return self._log

    def _get_colored_severity(self, severity: SeverityLevel) -> str:
        color = 'blue'
        if severity == 'warning':
            color = 'yellow'
        elif severity == 'error':
            color = 'red'

        if severity == 'information':
            severity = 'info'

        return f'[{color}]{severity.upper()}[/{color}] '

    def _write(
        self,
        message: str,
        title: str = '',
        severity: SeverityLevel = 'information',
    ) -> None:
        dt = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')
        msg = ''.join([
            f'{dt} {self._get_colored_severity(severity)}',
            f'{title}. {message}' if title else message,
        ])

        self.log.write(msg)
        if title:
            self.log.notify(message, title=title, severity=severity, timeout=7)

    def info(self, message: str, title: str = '') -> None:
        self._write(message, title)

    def warning(self, message: str, title: str = '') -> None:
        self._write(message, title, 'warning')

    def error(self, message: str, title: str = '', notification: bool = False) -> None:
        self._write(message, title, 'error')
