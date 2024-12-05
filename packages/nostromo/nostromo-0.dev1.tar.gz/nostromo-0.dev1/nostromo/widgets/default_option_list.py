import re
from asyncio import sleep
from copy import deepcopy
from datetime import datetime, UTC
from typing import List

from textual import events, work
from textual.reactive import reactive
from textual.widgets import OptionList


class DefaultOptionList(OptionList):
    DEFAULT_CSS = """
    .option-list--option {layer: above}
    DefaultOptionList {width: 52 !important}
    DefaultOptionList:focus {border: ascii #4577D4 60% !important}
    DefaultOptionList:focus > .option-list--option-highlighted {background: #4577D4 60%}
    """

    _options_copy = []
    _input_buffer = reactive('')
    _last_input_dt = datetime.now(UTC)
    value = reactive('')

    def on_mount(self):
        self._options_copy = deepcopy(self._options)
        self.clear_options()
        if self._options_copy:
            self.add_option(self._options_copy[0])
            self.value = self._options_copy[0].prompt

    def on_key(self, event: events.Key) -> None:
        if event.key == 'tab' and len(self._options) > 1:
            self.action_select()

        if re.fullmatch(r'[A-Za-z0-9]', event.key) or event.key == 'backspace':
            self.clear_options()
            if event.key == 'backspace':
                if len(self._input_buffer) == 1:
                    self._input_buffer = ''
                    self.action_select()
                    return

                self._input_buffer = self._input_buffer[:-1]
            else:
                self._input_buffer += event.key

            self.add_option(self._input_buffer)
            self._last_input_dt = datetime.now(UTC)
            self._find_options()

    @work(exclusive=True)
    async def _find_options(self):
        await sleep(0.5)
        self.clear_options()
        for option in self._options_copy:
            prompt = option if isinstance(option, str) else option.prompt
            if prompt.lower().find(self._input_buffer) > -1:
                self.add_option(option)

        if self._options:
            self.action_page_down()
        else:
            self.add_option(self._input_buffer)

        self._input_buffer = ''

    def action_select(self) -> None:
        # disabled select
        if len(self._options) == 1:
            selected = self.get_option_at_index(0)
            move = True
            self.clear_options()

            for ix, entrypoint in enumerate(self._options_copy):
                self.add_option(entrypoint)
                if move:
                    self.action_page_down()

                prompt = entrypoint if isinstance(entrypoint, str) else entrypoint.prompt
                if prompt == selected.prompt:
                    self.value = prompt
                    move = False

            return

        # opened with an option
        if self.highlighted:
            option = self.get_option_at_index(self.highlighted)
            self.clear_options()
            self.add_option(option)
            self.value = option.prompt
            return

        # init - show first
        if self._options_copy:
            self.clear_options()
            self.add_option(self._options_copy[0])
            self.value = self._options_copy[0]

    def reset_options(self, options: List[str]):
        self._options_copy = deepcopy(options)
        self.clear_options()
        if options:
            self.add_option(options[0])
