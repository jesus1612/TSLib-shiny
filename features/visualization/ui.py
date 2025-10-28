# Visualization feature UI components
from shiny import ui
from components.layout import create_card, create_metric_card

def render_visualization_ui() -> ui.Tag:
    """Render visualization step UI components"""
    
    # Single focused visualization section
    return create_card(
        title="📊 Visualización de Serie Temporal",
        subtitle="Gráfico interactivo y estadísticas básicas",
        content=ui.div(
            ui.div(
                ui.div("📊", class_="file-upload-icon"),
                ui.div("El gráfico se generará después de cargar los datos", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.input_action_button("refresh_plot", "🔄 Actualizar Gráfico", class_="btn btn-secondary"),
                    ui.input_action_button("zoom_in", "🔍 Zoom In", class_="btn btn-secondary"),
                    ui.input_action_button("zoom_out", "🔍 Zoom Out", class_="btn btn-secondary"),
                    class_="d-flex gap-2 mb-3"
                ),
                ui.div(
                    ui.div("Gráfico de serie temporal", id="time_series_plot"),
                    class_="plot-container"
                ),
                class_="mt-3"
            ),
            ui.div(
                ui.tags.h4("Estadísticas básicas:"),
                ui.div(
                    create_metric_card("0", "Media", "📊"),
                    create_metric_card("0", "Desv. Estándar", "📏"),
                    create_metric_card("0", "Mínimo", "⬇️"),
                    create_metric_card("0", "Máximo", "⬆️"),
                    class_="metrics-grid"
                ),
                class_="mt-3"
            )
        )
    )