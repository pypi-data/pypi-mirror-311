"""Provides a base modal dialog for showing text to the user."""

from rich.text import Text, TextType
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static
from textual.widgets._button import ButtonVariant

from .. import constants


class TextDialog(ModalScreen[None]):
    # Default CSS for the base text modal dialog.
    DEFAULT_CSS = """
    TextDialog {
        align: center middle;
    }

    TextDialog Center {
        width: 100%;
    }

    TextDialog > Vertical {
        background: $boost;
        min-width: 30%;
        width: auto;
        height: auto;
        border: round $primary;
    }

    TextDialog Static {
        width: auto;
    }

    TextDialog .spaced {
        padding: 1 4;
    }

    TextDialog #message {
        min-width: 100%;
    }
    """

    # Bindings for the base text modal dialog.
    BINDINGS = [
        Binding("escape", "dismiss(None)", "", show=False),
    ]

    def __init__(self, title: TextType, message: TextType) -> None:
        """Base modal dialog for showing information.

        Args:
            title: The title for the dialog.
            message: The message to show.
        """
        super().__init__()
        self._title = title
        self._message = message

    @property
    def button_style(self) -> ButtonVariant:
        # The style for the dialog's button.
        return "primary"

    def compose(self) -> ComposeResult:
        # Compose the content of the modal dialog.
        with Vertical():
            with Center():
                yield Static(self._title, classes="spaced")
            yield Static(self._message, id="message", classes="spaced")
            with Center(classes="spaced"):
                yield Button("OK", variant=self.button_style)

    def on_mount(self) -> None:
        # Configure the dialog once the DOM has loaded.
        self.query_one(Button).focus()

    def on_button_pressed(self) -> None:
        # Handle the OK button being pressed.
        self.dismiss(None)


class AboutDialog(TextDialog):
    DEFAULT_CSS = """
    TextDialog > Vertical {
        border: thick $primary 50%;
    }
    """

    def __init__(self) -> None:
        title = "About"
        message = Text.from_markup(
            f"Built with [@click=app.visit('https://github.com/textualize/textual')]Textual[/] "
            f"by [@click=app.visit('https://textualize.io')]Textualize[/].\n\n"
            f"Modified for use with ArgParse by [@click=app.visit('https://f2dv.com')]Fresh2.dev[/].\n\n"
            f"[@click=app.visit('https://github.com/fresh2dev/{constants.PACKAGE_NAME}')]"
            f"https://github.com/fresh2dev/{constants.PACKAGE_NAME}[/]",
        )
        super().__init__(title, message)
