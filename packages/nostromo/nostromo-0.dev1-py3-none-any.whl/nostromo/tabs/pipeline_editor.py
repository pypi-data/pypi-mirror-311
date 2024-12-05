from asyncio import sleep

import inject
from textual import work
from textual.app import ComposeResult
from textual.containers import Container
from textual.validation import Regex, Length
from textual.widget import Widget
from textual.widgets import Input, Button, Switch
from textual.widgets import Tree
from textual.widgets._tree import TreeNode, TreeDataType

from ..protocols.pipelines import PipelinesProtocol
from ..tcss import Class
from ..widgets.default_option_list import DefaultOptionList
from ..widgets.horizontal_form import HorizontalForm


class _EntrypointOptions(DefaultOptionList):
    DEFAULT_CSS = """
    _EntrypointOptions {layer: above}
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


class _CreateButton(Button):
    DEFAULT_CSS = """
    _CreateButton {border: round #00AF64 !important; opacity: 0.3 !important;}
    _CreateButton:focus { background: #1e1e1e !important; color: #00AF64 !important; }
    _CreateButton.-success {color: #00AF64 !important;}
    _CreateButton.-active {
        background: #00AF64 20% !important;
        border: round #00AF64 !important;
    }
    """

    def __init__(self, pipeline_editor_form: '_PipelineEditorForm'):
        self._pipeline_editor_form = pipeline_editor_form
        super().__init__('Create', 'success', name=None, id=None, classes=Class.BG, disabled=True, tooltip=None,
                         action=None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if str(event.button.label) == 'Create':
            self._pipeline_editor_form.create_tree_item()
            return

        self._pipeline_editor_form.update_tree_item()


class _PipelineEditorForm(HorizontalForm):
    def __init__(self, content: 'PipelineEditorContent'):
        self.content = content
        self.group = Switch(value=True, animate=False, name='Is group', id='type', disabled=True)
        self.name_input = Input(
            name='Name',
            placeholder='example: s3.files_upload',
            validators=[
                Regex('^[a-z0-9_.]*$',
                      failure_description='Group does not match regular expression ^\[a-z0-9_.]*$'),
                Length(3, 25),
            ],
            id='name',
        )

        self.group_type = DefaultOptionList(*['parallel', 'while', 'foreach'], id='group_type', name='Type')
        self.create_btn = _CreateButton(self)

        super().__init__(*[
            self.group,
            self.name_input,
            self.group_type,
            self.create_btn,
        ], name=None, id=None, classes=None, disabled=False)

    def set_node_name(self, name: str):
        self.name_input.value = name

    def _on_valid_form(self):
        self.create_btn.disabled = False
        self.create_btn.styles.opacity = 100

    def create_tree_item(self):
        if self.group.value:
            self.content.create_group(self._form_values['name'])
        else:
            self.content.create_task(self._form_values['name'])

        self.clear_inputs()
        self.name_input.focus()
        self.group.value = False

    def update_tree_item(self):
        self.content.tree.update_tree_item(self.name_input.value)
        self.content.tree.focus()

    def set_create_mode(self):
        self.name_input.value = ''
        self.create_btn.label = 'Create'
        self.group.disabled = False
        self.group.value = False
        self.group.styles.opacity = 100
        self.styles.opacity = 100
        self.name_input.focus()

    def set_update_mode(self, node: TreeNode):
        self.name_input.value = node.label.plain
        self.create_btn.label = 'Update'

        if node.allow_expand and node.expand:
            self.group.value = True
        else:
            self.group.value = False

        self.group.disabled = True
        self.group.styles.opacity = 0.4


class _PipelineTree(Tree):
    BINDINGS = [
        ('ctrl+a', 'append_node()', 'Append'),
        ('ctrl+d', 'delete_node()', 'Delete'),
    ]
    DEFAULT_CSS = """
    _PipelineTree {
        color: #c7c9ca !important;
        padding: 1 0 0 2;
        border-left: #1047A9 60% !important;
        border-top: #1047A9 60% !important;
        opacity: 0.8;
    }
    _PipelineTree .tree--highlight-line {background: #1e1e1e !important; color: orange !important;}
    _PipelineTree .tree--cursor {background: #1e1e1e !important; color: orange !important;}
    _PipelineTree .tree--guides {color: #1047A9}
    """

    def __init__(
        self,
        content: 'PipelineEditorContent',
        data: TreeDataType | None = None,
        *,
        label: str | None = None
     ) -> None:
        super().__init__(label=label, data=data, name='', id=None, classes=Class.BG, disabled=False)
        self.content = content

    def update_tree_item(self, name: str):
        self.cursor_node.label = name

    def on_focus(self):
        self.styles.opacity = 100
        self.content.form.styles.opacity = 0.6
        self.content.form.set_update_mode(self.cursor_node)

    def on_blur(self) -> None:
        self.styles.opacity = 0.7
        self.content.form.styles.opacity = 100

    def action_cursor_up(self) -> None:
        super().action_cursor_up()
        self.content.form.set_update_mode(self.cursor_node)

    def action_cursor_down(self) -> None:
        super().action_cursor_down()
        self.content.form.set_update_mode(self.cursor_node)

    def action_append_node(self):
        if self.cursor_node.allow_expand and self.cursor_node.expand:
            self.styles.opacity = 0.7
            self.content.form.set_create_mode()
            return

        self.notify(f'Active element - task "{self.cursor_node.label}". You can only add elements to groups',
                    title='Task error',
                    severity='error')

    def action_delete_node(self):
        self.cursor_node.remove()


class PipelineEditorContent(Widget):
    tree: _PipelineTree or None = None
    DEFAULT_CSS = """
    _PipelineEditorForm {width: 0.4fr !important; margin: 0 0 0 5}
    Tree {display: none}
    """

    @classmethod
    def get_id(cls):
        return 'PipelineEditor'

    def compose(self) -> ComposeResult:
        yield Container(
            _PipelineEditorForm(self),
            Container(id='tree'),
            classes='hl',
        )

    @property
    def create_btn(self) -> _CreateButton:
        return self.query_one(_CreateButton)

    def deactivate_create_btn(self):
        btn = self.create_btn
        btn.disabled = True
        btn.styles.opacity = 0.3

    @property
    def form(self) -> _PipelineEditorForm:
        return self.query_one(_PipelineEditorForm)

    def create_task(self, name: str):
        self.tree.cursor_node.add_leaf(name)
        self.deactivate_create_btn()

    def create_group(self, name: str):
        if self.tree:
            self.tree.cursor_node.add(name, expand=True)
        else:
            self.tree = _PipelineTree(content=self, label=name)
            self.load_tree(self.tree)

        self.deactivate_create_btn()

    @work(exclusive=True)
    async def load_tree(self, tree: Tree):
        container = self.query_one('#tree')
        container.set_loading(True)
        await sleep(0.4)
        await container.mount(tree)

        tree.root.expand()
        container.set_loading(False)
        tree.styles.display = 'block'
        self.query_one(Switch).disabled = False
