import inject
from textual import on
from textual.validation import Regex
from textual.widget import Widget
from textual.widgets import Input, Button, Footer, Pretty

from .protocols.path import PathProtocol
from .protocols.pipelines import PipelinesProtocol
from .protocols.ui_log import UILogProtocol
from .widgets.default_option_list import DefaultOptionList
from .widgets.horizontal_form import HorizontalForm


class _EntrypointOptions(DefaultOptionList):
    DEFAULT_CSS = """
    _EntrypointOptions {
        layer: above;
    }
    """
    _pipelines = inject.attr(PipelinesProtocol)

    def _reset_scripts_options(self):
        script_options: DefaultOptionList = self.parent.parent.query_one('#ScriptOptions')
        script_options.clear_options()
        options = self._pipelines.get_scripts_by_entrypoint(self.value)
        script_options.reset_options(options)

    def action_select(self) -> None:
        super().action_select()
        self._reset_scripts_options()


class PipelineBuilderWidget(Widget):
    _pipelines = inject.attr(PipelinesProtocol)
    _paths = inject.attr(PathProtocol)

    def compose(self) -> None:
        yield Footer()
        yield HorizontalForm(
            _EntrypointOptions(*self._pipelines.entrypoints, name='entrypoint'),
            DefaultOptionList(id='ScriptOptions', name='ScriptOptions'),
            Input(placeholder='calculate_events', name='Task Name', validators=[
                Regex('^[a-z0-9_]*$', failure_description='Task name does not match regular expression "^[a-z0-9_]*$"')
            ]),
            # Input(placeholder='--param1=value1 --param2=value2', name='Parameters'),
            RunCmdButton('Run', variant='success', name=''),
        )
        yield Pretty([])

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        # Updating the UI to show the reasons why validation failed
        if not event.validation_result.is_valid:
            self.query_one(Pretty).update(event.validation_result.failure_descriptions)
        else:
            self.query_one(Pretty).update([])


class RunCmdButton(Button):
    _log = inject.attr(UILogProtocol)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self._log.info('test', 'Run Script')
