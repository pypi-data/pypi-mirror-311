import abc
from typing import Protocol

from textual.scroll_view import ScrollView


class UILogProtocol(Protocol, metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def log(self) -> ScrollView:
        pass

    @abc.abstractmethod
    def info(self, message: str, title: str = '') -> None:
        pass

    @abc.abstractmethod
    def warning(self, message: str, title: str = '') -> None:
        pass

    @abc.abstractmethod
    def error(self, message: str, title: str = '') -> None:
        pass

