from asyncio import sleep
from typing import Callable

import inject
from rich.text import TextType
from textual import work
from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.widgets import Footer, Tab, Tabs

from .protocols.ui_log import UILogProtocol
from .screens.logs import LogsScreen
from .tabs.pipeline_editor import PipelineEditorContent
from .tabs.pipelines import PipelienesContent


class _MainTabs(Tabs):
    DEFAULT_CSS = """
    _MainTabs {layer: below; opacity: 0.5 !important}
    _MainTabs .underline--bar {background: orange 50% !important; color: orange !important}
    _MainTabs Tab {opacity: 0.6; color: #4577D4}
    _MainTabs Tab.-active, _MainTabs Tab.-active:hover {opacity: 1; color: orange !important}
    """

    def __init__(self, *tabs: Tab | TextType, active: str | None = None, name: str | None = None, id: str | None = None,
                 classes: str | None = None, disabled: bool = False, on_tab_callback: Callable):
        super().__init__(*tabs, active=active, name=name, id=id, classes=classes, disabled=disabled)
        self._on_tab_callback = on_tab_callback

    def watch_active(self, previously_active: str, active: str) -> None:
        super().watch_active(previously_active, active)
        self._on_tab_callback(active)

    @property
    def default_opacity(self) -> float:
        return 0.5

    def on_focus(self) -> None:
        # visual loading
        self.__on_focus()

    @work(exclusive=True)
    async def __on_focus(self):
        for tab in self.query(Tab):
            tab.disabled = False

        content = self.loaded_content
        self.styles.animate('opacity', value=100, duration=0.2)
        content.styles.animate('opacity', value=0.6, duration=0.2)
        await sleep(0.2)
        self.styles.opacity = 100
        content.styles.opacity = 0.6

    def on_blur(self) -> None:
        self.__on_blur()

    @work(exclusive=True)
    async def __on_blur(self):
        # visual loading
        loaded = self.loaded_content
        while loaded.styles.opacity != 0.6:
            await sleep(0.21)

        self.styles.animate('opacity', value=self.default_opacity, duration=0.1)
        await sleep(0.1)
        self.styles.opacity = self.default_opacity
        loaded.styles.opacity = 100

    @property
    def loaded_content(self) -> Widget:
        return self.parent.query_one(TabContent).children[0]


class TabContent(Widget):
    DEFAULT_CSS = """
    TabContent {padding: 1 1 1 1; opacity: 60 !important}
    """


class Nostromo(App):
    _log = inject.attr(UILogProtocol)
    _tab_content = TabContent()
    DEFAULT_CSS = """
    Screen {layers: below above; scrollbar-size-vertical: 1 !important; scrollbar-color: #4577D4 20% !important}
    Label {color: #c7c9ca; text-style: bold}
    .-textual-loading-indicator {background: #1e1e1e!important; color: orange}
    .vl {layout: vertical; height: auto}
    .hl {layout: horizontal; height: auto}
    .bg {background: #1e1e1e !important}
    Switch:focus, Switch:hover { border: solid #4577D4 60% !important}
    Switch.-on > .switch--slider { color: #00AF64 !important }
    """

    SCREENS = {'logs': LogsScreen}
    BINDINGS = [
        ('ctrl+l', 'push_screen("logs")', 'Logs'),
    ]

    def compose(self) -> ComposeResult:
        yield _MainTabs(
            Tab(PipelienesContent.get_id(), id=PipelienesContent.get_id(), disabled=False),
            Tab('Pipeline Editor', id=PipelineEditorContent.get_id(), disabled=False),
            on_tab_callback=self.open_tab,
        )

        self._tab_content.styles.layer = 'below'
        self._tab_content.display = 'none'  # visual loading
        yield self._tab_content
        yield Footer()
        self.open_tab(PipelienesContent.get_id())

    @work(exclusive=True)
    async def open_tab(self, tab_id: str):
        # inject + mount waiting
        while not self._tab_content or not self._tab_content.is_mounted:
            await sleep(0.2)
            break
        # mounted

        await self._tab_content.remove_children()
        self._tab_content.display = 'block'  # visual loading
        self._tab_content.set_loading(True)

        for tab_content in (
            PipelienesContent,
            PipelineEditorContent,
        ):
            if tab_content.get_id() != tab_id:
                continue

            content = tab_content()
            content.styles.opacity = 0
            await self._tab_content.mount(content)
            await sleep(0.3)  # visual loading
            self._tab_content.set_loading(False)

            content.styles.animate('opacity', value=0.6, duration=0.2)
            await sleep(0.2)  # visual loading
            content.styles.opacity = 0.6
            break
