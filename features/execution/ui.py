# Execution feature UI components
from shiny import ui
from components.layout import create_card

def render_execution_ui() -> ui.Tag:
    """Render execution step UI components"""
    
    return create_card(
        title="🚀 Ejecución del Análisis",
        subtitle="Inicia el procesamiento de modelos",
        content=ui.div(
            ui.div(
                ui.input_action_button("start_execution", "▶️ Iniciar Análisis", class_="btn btn-primary btn-lg"),
                ui.input_action_button("pause_execution", "⏸️ Pausar", class_="btn btn-warning"),
                ui.input_action_button("stop_execution", "⏹️ Detener", class_="btn btn-danger"),
                class_="d-flex gap-2 mb-3"
            ),
            ui.div(
                ui.div("Estado: Listo para ejecutar", id="execution_status", class_="status-indicator status-info execution-status"),
                ui.div("Tiempo estimado: 2-5 minutos", id="estimated_time", class_="estimated-time"),
                class_="mt-2"
            ),
            ui.div(
                ui.tags.h4("Progreso:"),
                ui.div(
                    ui.div("Preparando...", class_="progress-step"),
                    ui.div("Ajustando modelos...", class_="progress-step"),
                    ui.div("Validando...", class_="progress-step"),
                    ui.div("Finalizando...", class_="progress-step"),
                    class_="progress-list"
                ),
                class_="mt-3"
            )
        )
    )