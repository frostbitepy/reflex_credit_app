import reflex as rx
import os
from .components.forms import main_form, FormState


def index() -> rx.Component:
    return rx.box(
        rx.vstack(
            main_form(FormState),
            spacing="4",  # Changed from "1.5em" to "4"
            font_size="1em",
            padding="2em",
        )
    )

# Initialize the app with the base state
app = rx.App()
app.add_page(
    index,
    route="/",
    title="Sistema de Evaluación Crediticia",
    )