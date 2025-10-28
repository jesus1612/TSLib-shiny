# Model selection feature UI components
from shiny import ui
from components.layout import create_card, create_form_group

def render_model_selection_ui() -> ui.Tag:
    """Render model selection step UI components"""
    
    return create_card(
        title="⚙️ Configuración de Modelo ARIMA",
        subtitle="Selecciona los parámetros del modelo",
        content=ui.div(
            ui.div(
                ui.input_switch("auto_arima", "Selección automática", value=True),
                ui.tags.p("Activar para selección automática de parámetros", class_="text-muted"),
                class_="mb-3"
            ),
            ui.div(
                ui.div(
                    create_form_group(
                        label="Orden AR (p)",
                        control=ui.input_numeric("ar_order", "Orden AR", value=1, min=0, max=10),
                        help_text="Número de términos autorregresivos"
                    ),
                    create_form_group(
                        label="Orden MA (q)",
                        control=ui.input_numeric("ma_order", "Orden MA", value=1, min=0, max=10),
                        help_text="Número de términos de media móvil"
                    ),
                    class_="col-md-6"
                ),
                ui.div(
                    create_form_group(
                        label="Diferenciación (d)",
                        control=ui.input_numeric("diff_order", "Orden de diferenciación", value=1, min=0, max=3),
                        help_text="Número de diferencias para estacionariedad"
                    ),
                    create_form_group(
                        label="Paralelización",
                        control=ui.input_slider("n_jobs", "Número de trabajos paralelos", min=1, max=8, value=4),
                        help_text="Número de procesos paralelos para optimización"
                    ),
                    class_="col-md-6"
                ),
                class_="row"
            )
        )
    )