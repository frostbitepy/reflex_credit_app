import reflex as rx
from typing import List
from ..components.data_loader import data_loader_component, DataLoaderState
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
WIDTH = "30%"
BADGE_COLOR = "primary"
BADGE_WIDTH = "100%"
BADGE_VARIANT = "soft"

class FormState(rx.State):
    persona: str = ""
    nombre: str = ""
    ci: str = ""
    perfil_comercial: str = ""
    fecha_nacimiento: str = ""
    edad: int = 0
    ingresos: float = 0.0
    antiguedad_laboral: str = ""
    posee_bienes: str = ""
    empresa: str = ""
    faja: str = ""
    producto: str = ""
    monto_solicitado: float = 0.0
    cuota: float = 0.0
    plazo: int = 0
    garantia: str = ""
    deuda_financiera: float = 0.0
    comentarios: str = ""
    form_data = {}

    @rx.event
    def handle_submit(self, form_data: dict):
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

        # Print the results
        print(f"Puntaje Final: {puntaje_final}")
        print(f"Recomendación: {recomendacion}")

    @rx.event
    def change_value(self, value: str, name: str):
        setattr(self, name, value)

    @rx.event
    async def update_deuda_financiera(self, value: float):
        self.deuda_financiera = value

def main_form() -> rx.Component:
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.heading("Formulario de Solicitud de Crédito", level=2, align="center", size="7"),
                rx.heading("Datos del Solicitante", level=3, size="5"),
                rx.hstack(
                    rx.select(
                        PERSONA_OPTIONS,
                        value=PERSONA_OPTIONS[0],
                        on_change=lambda value: FormState.change_value(value, "persona"),
                        width=WIDTH,
                    ),
                    rx.select(
                        PERFIL_COMERCIAL_OPTIONS,
                        value=PERFIL_COMERCIAL_OPTIONS[0],
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
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.divider(),
                rx.heading("Datos de Evaluación", level=3, size="5"),
                rx.hstack(
                    rx.input(
                        placeholder="Ingresos",
                        value=str(FormState.ingresos),
                        on_change=lambda value: FormState.change_value(value, "ingresos"),
                        type="number",
                        width=WIDTH,
                    ),
                    rx.select(
                        ANTIGUEDAD_OPTIONS,
                        value=ANTIGUEDAD_OPTIONS[0],
                        on_change=lambda value: FormState.change_value(value, "antiguedad_laboral"),
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.select(
                        BIENES_OPTIONS,
                        value=BIENES_OPTIONS[0],
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
                        value=PRODUCTO_OPTIONS[0],
                        on_change=lambda value: FormState.change_value(value, "producto"),
                        width=WIDTH,
                    ),
                    rx.input(
                        placeholder="Monto Solicitado",
                        value=str(FormState.monto_solicitado),
                        on_change=lambda value: FormState.change_value(value, "monto_solicitado"),
                        type="number",
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.input(
                        placeholder="Cuota",
                        value=str(FormState.cuota),
                        on_change=lambda value: FormState.change_value(value, "cuota"),
                        type="number",
                        width=WIDTH,
                    ),
                    rx.input(
                        placeholder="Plazo (meses)",
                        value=str(FormState.plazo),
                        on_change=lambda value: FormState.change_value(value, "plazo"),
                        type="number",
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.hstack(
                    rx.select(
                        GARANTIA_OPTIONS,
                        value=GARANTIA_OPTIONS[0],
                        on_change=lambda value: FormState.change_value(value, "garantia"),
                        width=WIDTH,
                    ),
                    width="100%",
                ),
                rx.divider(),
                rx.input(
                    placeholder="Deuda Financiera",
                    value=str(FormState.deuda_financiera),
                    on_change=lambda value: FormState.change_value(value, "deuda_financiera"),
                    type="number",
                    width=WIDTH,
                ),
                rx.heading("Excel File Upload and Operations", level=3, align="center"),
                # En forms.py, dentro de main_form()
                data_loader_component(),
                rx.divider(),
                rx.input(
                    placeholder="Comentarios",
                    value=FormState.comentarios,
                    on_change=lambda value: FormState.change_value(value, "comentarios"),
                    width=WIDTH,
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=FormState.handle_submit,
            reset_on_submit=True,
        ),
        rx.divider(),
    )