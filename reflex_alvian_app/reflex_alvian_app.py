import reflex as rx
from .components.forms import main_form, FormState
from .components.data_loader import DataLoaderState

class State(rx.State):
    """The app state."""
    pass

def index() -> rx.Component:
    return rx.box(
        rx.vstack(
            main_form(),
            spacing="4",  # Changed from "1.5em" to "4"
            font_size="1em",
            padding="2em",
        )
    )

# Initialize the app
app = rx.App()
app.add_page(index)