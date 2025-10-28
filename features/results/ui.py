# Results feature UI components
from shiny import ui
from components.layout import create_card, create_metric_card

def render_results_ui() -> ui.Tag:
    """Render results step UI components"""
    
    return create_card(
        title="📈 Resultados del Análisis",
        subtitle="Métricas y predicciones del modelo",
        content=ui.div(
            ui.div(
                ui.div("📊", class_="file-upload-icon"),
                ui.div("Los resultados se mostrarán después de la ejecución", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.tags.h4("Métricas de evaluación:"),
                    ui.div(
                        create_metric_card("1234.56", "AIC", "📊"),
                        create_metric_card("1256.78", "BIC", "📊"),
                        create_metric_card("15.23", "RMSE", "📏"),
                        create_metric_card("12.45", "MAE", "📏"),
                        class_="metrics-grid"
                    ),
                    class_="mt-3"
                ),
                ui.div(
                    ui.tags.h4("Predicciones:"),
                    ui.div("Gráfico de predicciones", id="forecast_plot"),
                    class_="mt-3"
                ),
                ui.div(
                    ui.input_action_button("export_results", "💾 Exportar Resultados", class_="btn btn-primary"),
                    class_="mt-3"
                )
            )
        )
    )