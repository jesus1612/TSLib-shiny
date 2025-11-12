# Model selection feature UI components
from shiny import ui
from components.layout import create_card, create_form_group

def render_model_selection_ui() -> ui.Tag:
    """Render model selection step UI components"""
    
    return create_card(
        title="⚙️ Selección de Modelo",
        subtitle="Configura el modelo de series temporales",
        content=ui.div(
            # Model type selector
            ui.div(
                ui.tags.h5("Tipo de Modelo:"),
                ui.input_radio_buttons(
                    "model_type",
                    "",
                    choices={
                        "AR": "AR - Autoregresivo",
                        "MA": "MA - Media Móvil",
                        "ARMA": "ARMA - Combinado",
                        "ARIMA": "ARIMA - Integrado"
                    },
                    selected="ARIMA"
                ),
                ui.output_ui("model_description"),
                class_="mb-4"
            ),
            # Auto-selection switch
            ui.div(
                ui.input_switch("auto_select", "Selección automática de orden", value=True),
                ui.tags.p("Activar para que el modelo seleccione automáticamente los parámetros óptimos", class_="text-muted"),
                class_="mb-4"
            ),
            # Manual parameters (shown when auto_select is False)
            ui.output_ui("manual_parameters_ui"),
            # Additional options
            ui.div(
                ui.tags.h5("Opciones Adicionales:"),
                create_form_group(
                    label="Pasos a Pronosticar",
                    control=ui.input_numeric("forecast_steps", "", value=10, min=1, max=100),
                    help_text="Número de pasos futuros a predecir"
                ),
                ui.input_switch("include_confidence", "Incluir intervalos de confianza", value=True),
                class_="mt-3"
            )
        )
    )