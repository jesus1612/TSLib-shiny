# Results feature UI components
from shiny import ui
from components.layout import create_card, create_metric_card

def render_results_ui() -> ui.Tag:
    """Render results step UI components"""
    
    return create_card(
        title="📈 Resultados del Análisis",
        subtitle="Métricas y predicciones del modelo",
        content=ui.div(
            # Model info
            ui.div(
                ui.tags.h5("Información del Modelo:"),
                ui.output_ui("model_info_ui"),
                class_="mb-4"
            ),
            # Metrics
            ui.div(
                ui.tags.h5("Métricas de Evaluación:"),
                ui.output_ui("metrics_cards"),
                class_="mb-4"
            ),
            # Forecast plot
            ui.div(
                ui.tags.h5("Pronóstico:"),
                ui.output_plot("forecast_plot", height="400px"),
                class_="mb-4"
            ),
            # Forecast table
            ui.div(
                ui.tags.h5("Valores del Pronóstico:"),
                ui.output_ui("forecast_table_ui"),
                class_="mb-4"
            ),
            # Diagnostics
            ui.div(
                ui.tags.h5("Diagnósticos del Modelo:"),
                ui.div(
                    ui.div(
                        ui.output_plot("residuals_plot", height="300px"),
                        class_="col-md-6"
                    ),
                    ui.div(
                        ui.output_plot("residuals_acf_plot", height="300px"),
                        class_="col-md-6"
                    ),
                    class_="row"
                ),
                class_="mb-4"
            ),
            # Export button
            ui.div(
                ui.input_action_button("export_results", "💾 Exportar Resultados (CSV)", class_="btn btn-primary"),
                class_="text-center"
            )
        )
    )