from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import Label, Input, Button


class HorizontalForm(Widget):
    DEFAULT_CSS = """
    .error {color: #FF6440 !important}
    .hl Label {padding: 1 0 0 0}

    .-invalid {border: solid #FF6440 60% !important; color: #FF6440 !important}
    .-invalid:focus {border: solid #FF6440 60% !important; color: #FF6440 !important}
    
    Input {border: solid #4577D4 0% !important; margin-left: 1 !important; max-width: 50 !important}
    Input:focus {border: solid #4577D4 60% !important; color: #4577D4}
    """

    def __init__(self, *form_items: Widget, name: str | None = None, id: str | None = None, classes: str | None = None,
                 disabled: bool = False) -> None:
        super().__init__(*[], name=name, id=id, classes=classes, disabled=disabled)
        self._form_items = form_items
        self._errors_by_name = {}
        self._form_values = {}

    def compose(self) -> ComposeResult:
        max_label_width = max([len(w.name) for w in self._form_items if not isinstance(w, Button)]) + 1

        fields = []
        for field in self._form_items:
            if isinstance(field, Button):
                field.styles.margin = [0, 0, 0, 15]
                fields.append(field)
                continue

            label = Label(field.name)
            label.styles.width = max_label_width
            fields.append(Container(
                label,
                field,
                classes='hl',
            ))

            error_label = Label(id=f'{field.id}-error')
            error_label.styles.margin = [0, 0, 0, max_label_width + 1]
            fields.append(error_label)

        yield Container(*fields, classes='vl')

    def clear_inputs(self):
        for field in self._form_items:
            if isinstance(field, Input):
                field.value = ''

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        input_id = event.input.id
        self._form_values[input_id] = event.input.value
        self._errors_by_name.setdefault(input_id, [])
        self._errors_by_name[input_id] = event.validation_result.failure_descriptions

        for field, errors in self._errors_by_name.items():
            error = self.query_one(f'#{field}-error')
            error.remove_children()
            for msg in errors:
                error.mount(Label(msg, classes='error'))

        if not all(self._errors_by_name.values()):
            self._on_valid_form()

    def _on_valid_form(self):
        pass
