import reflex as rx
import pandas as pd
import datetime
from ..utils.pdf_maker import generate_detailed_pdf
from typing import List
from ..utils.calculos import (
    calcular_calificacion_final
)

# Constants
PERSONA_OPTIONS = ['Persona Física', 'Persona Jurídica']
ANTIGUEDAD_OPTIONS = ["6 meses a un año", "1 a 2 años", "3 a 5 años", "Más de 5 años"]
GARANTIA_OPTIONS = ["ASF", "Hipotecaria", "Prendaria", "Codeudoría"]
PERFIL_COMERCIAL_OPTIONS = ['Asalariado', 'Profesional Independiente']
BIENES_OPTIONS = ['No', 'Vehículo', 'Inmueble', 'Vehículo e Inmueble']
PRODUCTO_OPTIONS = ["Producto 1", "Producto 2", "Producto 3"]
WIDTH="50%"
BADGE_COLOR = "primary"
BADGE_WIDTH = "100%"
BADGE_VARIANT = "soft"

class FormState(rx.State):
    # Select fields with default values
    persona: str = PERSONA_OPTIONS[0]
    perfil_comercial: str = PERFIL_COMERCIAL_OPTIONS[0]
    antiguedad_laboral: str = ANTIGUEDAD_OPTIONS[0]
    posee_bienes: str = BIENES_OPTIONS[0]
    producto: str = PRODUCTO_OPTIONS[0]
    garantia: str = GARANTIA_OPTIONS[0]
    
    # Text input fields
    nombre: str = ""
    ci: str = ""
    fecha_nacimiento: str = ""
    empresa: str = ""
    faja: str = ""
    comentarios: str = ""
    
    # Numeric fields
    edad: int = 0
    ingresos: float = 0.0
    monto_solicitado: float = 0.0
    cuota: float = 0.0
    plazo: int = 0
    deuda_financiera: float = 0.0
    
    # File handling fields
    excel_filename: str = ""
    last_generated_pdf: str = ""
    
    # Form data storage
    form_data: dict = {}

    # Result values
    mostrar_resultados: bool = False
    puntaje_final: float = 0.0
    recomendacion: str = ""

    @rx.event
    def handle_submit(self, form_data: dict):
        """Procesar el formulario y mostrar resultados"""
        self.form_data = {
            "persona": getattr(self, "persona", ""),
            "nombre": getattr(self, "nombre", ""),
            "ci": getattr(self, "ci", ""),
            "perfil_comercial": getattr(self, "perfil_comercial", ""),
            "edad": getattr(self, "edad", 0),
            "ingresos": getattr(self, "ingresos", 0.0),
            "antiguedad_laboral": getattr(self, "antiguedad_laboral", ""),
            "posee_bienes": getattr(self, "posee_bienes", ""),
            "empresa": getattr(self, "empresa", ""),
            "faja": getattr(self, "faja", ""),
            "producto": getattr(self, "producto", ""),
            "monto_solicitado": getattr(self, "monto_solicitado", 0.0),
            "cuota": getattr(self, "cuota", 0.0),
            "plazo": getattr(self, "plazo", 0),
            "garantia": getattr(self, "garantia", ""),
            "deuda_financiera": getattr(self, "deuda_financiera", 0.0),
            "comentarios": getattr(self, "comentarios", ""),
        }

        # Calculate final score
        puntaje_final, recomendacion = calcular_calificacion_final(
            self.edad,
            self.ingresos,
            self.faja,
            self.antiguedad_laboral,
            self.posee_bienes,
            self.deuda_financiera,
            self.cuota
        )

        # Guardar resultados en el estado
        self.puntaje_final = puntaje_final
        self.recomendacion = recomendacion
        self.mostrar_resultados = True

    @rx.event
    def generate_and_download_pdf(self):
        """Generar y descargar el PDF con los resultados"""
        try:
            ratio_deuda_ingresos = round(self.deuda_financiera / self.ingresos, 2) if self.ingresos > 0 else 0

            # Generate PDF
            pdf_buffer = generate_detailed_pdf(
                nombre=self.nombre,
                profesion=self.perfil_comercial,
                ingresos=self.ingresos,
                fecha_nacimiento=self.fecha_nacimiento or "No especificada",
                empresa=self.empresa,
                perfil_comercial=self.perfil_comercial,
                producto=self.producto,
                monto_solicitado=self.monto_solicitado,
                plazo=self.plazo,
                cuota=self.cuota,
                garantia=self.garantia,
                scoring=self.faja,
                deuda_financiera=self.deuda_financiera,
                ratio_deuda_ingresos=ratio_deuda_ingresos,
                puntaje=self.puntaje_final,
                dictamen=self.recomendacion,
                comentarios=self.comentarios
            )

            # Generate filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dictamen_credito_{self.nombre.replace(' ', '_')}_{timestamp}.pdf"

            # Save to upload directory
            upload_path = rx.get_upload_dir() / filename
            upload_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(upload_path, "wb") as f:
                f.write(pdf_buffer.getvalue())

            # Store the filename for later download
            self.last_generated_pdf = filename
            
            # Return download URL
            return rx.download(url=f"/upload/{filename}")
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return None

    @rx.event
    def reset_form(self):
        """Resetear todos los valores del formulario"""
        # Reset select fields
        self.persona = PERSONA_OPTIONS[0]
        self.perfil_comercial = PERFIL_COMERCIAL_OPTIONS[0]
        self.antiguedad_laboral = ANTIGUEDAD_OPTIONS[0]
        self.posee_bienes = BIENES_OPTIONS[0]
        self.producto = PRODUCTO_OPTIONS[0]
        self.garantia = GARANTIA_OPTIONS[0]
        
        # Reset text fields
        self.nombre = ""
        self.ci = ""
        self.fecha_nacimiento = ""
        self.empresa = ""
        self.faja = ""
        self.comentarios = ""
        
        # Reset numeric fields
        self.edad = 0
        self.ingresos = 0.0
        self.monto_solicitado = 0.0
        self.cuota = 0.0
        self.plazo = 0
        self.deuda_financiera = 0.0
        
        # Reset file fields
        self.excel_filename = ""
        self.last_generated_pdf = ""
        
        # Reset results
        self.mostrar_resultados = False
        self.puntaje_final = 0.0
        self.recomendacion = ""
        self.form_data = {}

    @rx.event
    def change_value(self, value: str, name: str):
        """Convert and set form values with proper types."""
        try:
            # Handle type conversions based on field name
            if name == "edad" or name == "plazo":
                value = int(value) if value else 0
            elif name in ["ingresos", "monto_solicitado", "cuota"]:
                value = float(value) if value else 0.0
            
            # Set the converted value
            setattr(self, name, value)
            
        except (ValueError, TypeError) as e:
            print(f"Error converting value '{value}' for field '{name}': {str(e)}")

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle file upload and process Excel data."""
        try:
            if not files:
                return
                
            current_file = files[0]
            upload_data = await current_file.read()
            outfile = rx.get_upload_dir() / current_file.filename

            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            self.excel_filename = current_file.filename
            self.load_excel_data(outfile)
            
        except Exception as e:
            print(f"Error handling file upload: {str(e)}")
            self.excel_filename = ""
            self.deuda_financiera = 0.0

    def load_excel_data(self, file_path):
        """Load and process Excel data."""
        try:
            data_frame = pd.read_excel(file_path)
            self.deuda_financiera = float(data_frame.iloc[1:, 4].sum())
            print(f"Deuda Financiera actualizada: {self.deuda_financiera:,.2f}")
        except Exception as e:
            print(f"Error al procesar el archivo Excel: {str(e)}")
            self.deuda_financiera = 0.0

    def get_str_value(self, value, default=""):
        """Helper method to safely convert values to string."""
        try:
            return str(value) if value not in [None, 0, 0.0] else default
        except:
            return default

def main_form(FormState) -> rx.Component:
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.heading("Formulario de Solicitud de Crédito", level=2, align="center", size="7"),
                rx.heading("Datos del Solicitante", level=3, size="5"),
                rx.hstack(
                    rx.select(
                        PERSONA_OPTIONS,
                        value=FormState.persona | PERSONA_OPTIONS[0],
                        on_change=lambda value: FormState.change_value(value, "persona"),
                        width=WIDTH,
                    ),
                    rx.select(
                        PERFIL_COMERCIAL_OPTIONS,
                        value=FormState.perfil_comercial | PERFIL_COMERCIAL_OPTIONS[0],
                        on_change=lambda value: FormState.change_value(value, "perfil_comercial"),
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Nombre y Apellido",
                        value=FormState.nombre,
                        on_change=lambda value: FormState.change_value(value, "nombre"),
                        width=WIDTH,
                    ),
                    rx.input(
                        placeholder="Cédula de Identidad/RUC",
                        value=FormState.ci,
                        on_change=lambda value: FormState.change_value(value, "ci"),
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Edad",
                        on_change=lambda value: FormState.change_value(value, "edad"),
                        type="number",
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.divider(),
                rx.heading("Datos de Evaluación", level=3, size="5"),
                rx.hstack(
                    rx.input(
                        placeholder="Ingresos",
                        on_change=lambda value: FormState.change_value(value, "ingresos"),
                        type="number",
                        width=WIDTH,
                    ),
                    rx.select(
                        ANTIGUEDAD_OPTIONS,
                        value=FormState.antiguedad_laboral | ANTIGUEDAD_OPTIONS[0],
                        on_change=lambda value: FormState.change_value(value, "antiguedad_laboral"),
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.select(
                        BIENES_OPTIONS,
                        value=FormState.posee_bienes | BIENES_OPTIONS[0],
                        on_change=lambda value: FormState.change_value(value, "posee_bienes"),
                        width=WIDTH,
                    ),
                    rx.input(
                        placeholder="Empresa",
                        value=FormState.empresa,
                        on_change=lambda value: FormState.change_value(value, "empresa"),
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Faja Scoring Informconf",
                        value=FormState.faja,
                        on_change=lambda value: FormState.change_value(value, "faja"),
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.divider(),
                rx.heading("Datos de la Operación", level=3, size="5"),
                rx.hstack(
                    rx.select(
                        PRODUCTO_OPTIONS,
                        value=FormState.producto | PRODUCTO_OPTIONS[0],
                        on_change=lambda value: FormState.change_value(value, "producto"),
                        width=WIDTH,
                    ),
                    rx.input(
                        placeholder="Monto Solicitado",
                        on_change=lambda value: FormState.change_value(value, "monto_solicitado"),
                        type="number",
                        width=WIDTH,
                    ),
                        width="100%",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Monto Cuota",
                        on_change=lambda value: FormState.change_value(value, "cuota"),
                        type="number",
                        width=WIDTH,
                    ),
                    rx.input(
                        placeholder="Plazo (meses)",
                        on_change=lambda value: FormState.change_value(value, "plazo"),
                        type="number",
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.select(
                        GARANTIA_OPTIONS,
                        value=FormState.garantia | GARANTIA_OPTIONS[0],
                        on_change=lambda value: FormState.change_value(value, "garantia"),
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.divider(),
                rx.heading("Carga de Deuda Financiera", level=3, align="center", size="5"),
                rx.vstack(  # Changed from rx.form to rx.vstack
                    rx.upload(
                        rx.vstack(
                            rx.button(
                                "Seleccionar Archivo Excel",
                                type="button",
                            ),
                            rx.text("Arrastre el archivo aquí o haga clic para seleccionar", size="2"),
                        ),
                        id="upload1",
                        max_files=1,
                        padding="0.5em",
                    ),
                    rx.text(rx.selected_files("upload1"), size="1"),
                    rx.hstack(
                        rx.button(
                            "Calcular Deuda",
                            type="button",
                            on_click=lambda: FormState.handle_upload(rx.upload_files("upload1")),
                        ),
                        #rx.button(
                        #    "Limpiar",
                        #    type="button",
                        #    on_click=lambda: rx.clear_selected_files("upload1"),
                        #),
                        spacing="2",
                        padding="0.2em",
                    ),
                ),
                rx.cond(
                    FormState.excel_filename != "",
                    rx.vstack(
                        rx.text("Deuda Financiera/Comercial calculada:", font_weight="bold"),
                        rx.text(f"Gs. {FormState.deuda_financiera:,.0f}"),
                        padding="0.5em",
                    ),
                ),                
                rx.divider(),
                rx.input(
                    placeholder="Comentarios",
                    value=FormState.comentarios,
                    on_change=lambda value: FormState.change_value(value, "comentarios"),
                    width=WIDTH,
                ),
                rx.cond(
                    FormState.mostrar_resultados,
                    rx.vstack(
                        rx.heading("Resultados de la Evaluación", size="5", align="center"),
                        rx.box(
                            rx.vstack(
                                rx.text(f"Puntaje Final: {FormState.puntaje_final}", size="4"),
                                rx.text(f"Recomendación: {FormState.recomendacion}", size="4"),
                                spacing="4",
                                padding="2em",
                                border="1px solid",
                                border_color="gray.200",
                                border_radius="md",
                            )
                        ),
                        rx.hstack(
                            rx.button(
                                "Generar y Descargar PDF",
                                type="button",
                                bg="green.500",
                                color="white",
                                _hover={"bg": "green.600"},
                                on_click=FormState.generate_and_download_pdf,
                            ),
                            rx.button(
                                "Nueva Solicitud",
                                type="button",
                                bg="blue.500",
                                color="white",
                                _hover={"bg": "blue.600"},
                                on_click=FormState.reset_form,
                            ),
                            spacing="4",
                            padding="1em",
                        ),
                    ),
                    rx.button(
                        "Procesar Solicitud",
                        type="submit",
                        bg="blue.500",
                        color="white",
                        _hover={"bg": "blue.600"},
                        width="200px",
                    ),
                ),
            ),
            on_submit=FormState.handle_submit,
            reset_on_submit=True,
        ),
        rx.divider(),
    )