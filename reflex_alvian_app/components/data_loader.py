import reflex as rx
import pandas as pd
from io import BytesIO

class DataLoaderState(rx.State):
    data_file: str = ""
    data_frame: pd.DataFrame = pd.DataFrame()
    sumatoria_columna_5: float = 0.0

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle file upload and process Excel data."""
        current_file = files[0]
        upload_data = await current_file.read()
        outfile = rx.get_upload_dir() / current_file.filename

        with outfile.open("wb") as file_object:
            file_object.write(upload_data)

        self.data_file = current_file.filename
        self.load_excel_data(outfile)

    def load_excel_data(self, file_path):
        """Load and process Excel data."""
        self.data_frame = pd.read_excel(file_path)
        self.perform_operations()

    def perform_operations(self):
        """Process Excel data and update form."""
        print(self.data_frame.head())
        self.sumatoria_columna_5 = self.data_frame.iloc[1:, 4].sum()
        print(f"Sumatoria de la columna 5: {self.sumatoria_columna_5}")
        # Update form state through parent state
        self.parent_state.form_state.update_deuda_financiera(self.sumatoria_columna_5)

def data_loader_component() -> rx.Component:
    """Excel file upload component."""
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button("Select File"),
                rx.text("Drag and drop files here or click to select files"),
            ),
            id="upload1",
            max_files=1,
            padding="5em",
        ),
        rx.text(rx.selected_files("upload1")),
        rx.button(
            "Upload",
            on_click=lambda: DataLoaderState.handle_upload(
                rx.upload_files(upload_id="upload1")
            ),
        ),
        rx.button(
            "Clear",
            on_click=rx.clear_selected_files("upload1")
        ),
        rx.cond(
            DataLoaderState.data_file,
            rx.text(f"Sumatoria de la columna 5: {DataLoaderState.sumatoria_columna_5}"),
        ),
        padding="5em",
    )