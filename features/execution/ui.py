# Execution feature UI components
from shiny import ui
from components.layout import create_card, create_progress_bar, create_status_badge

def render_execution_ui() -> ui.Tag:
    """Render execution step UI components"""
    
    # Execution control section
    control_section = create_card(
        title="🚀 Control de Ejecución",
        subtitle="Iniciar y monitorear el proceso de modelado",
        content=ui.div(
            ui.div(
                ui.div(
                    ui.input_action_button("start_execution", "▶️ Iniciar Análisis", class_="btn btn-primary btn-lg"),
                    ui.input_action_button("pause_execution", "⏸️ Pausar", class_="btn btn-warning"),
                    ui.input_action_button("stop_execution", "⏹️ Detener", class_="btn btn-danger"),
                    class_="d-flex gap-2 mb-3"
                ),
                ui.div(
                    ui.div("Estado: Listo para ejecutar", id="execution_status", class_="status-indicator status-info"),
                    ui.div("Tiempo estimado: 2-5 minutos", id="estimated_time", class_="text-muted"),
                    class_="mt-2"
                )
            )
        )
    )
    
    # Progress tracking section
    progress_section = create_card(
        title="📊 Progreso de Ejecución",
        subtitle="Seguimiento del proceso de modelado",
        content=ui.div(
            ui.div(
                ui.div("⏳", class_="file-upload-icon"),
                ui.div("El progreso se mostrará durante la ejecución", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Progreso general:"),
                    create_progress_bar(0, 100, "Iniciando..."),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Etapas del proceso:"),
                    ui.div(
                        ui.div(
                            ui.div("✓", class_="status-indicator status-success"),
                            ui.div("Carga de datos", class_="step-label"),
                            class_="step-item"
                        ),
                        ui.div(
                            ui.div("⏳", class_="status-indicator status-warning"),
                            ui.div("Preprocesamiento", class_="step-label"),
                            class_="step-item"
                        ),
                        ui.div(
                            ui.div("⏸️", class_="status-indicator status-info"),
                            ui.div("Ajuste de modelos", class_="step-label"),
                            class_="step-item"
                        ),
                        ui.div(
                            ui.div("⏸️", class_="status-indicator status-info"),
                            ui.div("Validación", class_="step-label"),
                            class_="step-item"
                        ),
                        ui.div(
                            ui.div("⏸️", class_="status-indicator status-info"),
                            ui.div("Generación de resultados", class_="step-label"),
                            class_="step-item"
                        ),
                        class_="steps-list"
                    ),
                    class_="mt-3"
                ),
                id="progress_content",
                class_="d-none"
            )
        )
    )
    
    # Real-time log section
    log_section = create_card(
        title="📝 Log de Ejecución",
        subtitle="Registro en tiempo real del proceso",
        content=ui.div(
            ui.div(
                ui.div("📄", class_="file-upload-icon"),
                ui.div("El log se mostrará durante la ejecución", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.div(
                        ui.input_action_button("clear_log", "🗑️ Limpiar Log", class_="btn btn-secondary"),
                        ui.input_action_button("export_log", "💾 Exportar Log", class_="btn btn-secondary"),
                        ui.input_switch("auto_scroll", "Auto-scroll", value=True),
                        class_="d-flex gap-2 mb-3"
                    ),
                    ui.div(
                        ui.div(
                            ui.div("2024-01-15 10:30:15 - Iniciando análisis...", class_="log-entry"),
                            ui.div("2024-01-15 10:30:16 - Cargando datos desde archivo...", class_="log-entry"),
                            ui.div("2024-01-15 10:30:17 - Datos cargados: 1000 observaciones", class_="log-entry"),
                            ui.div("2024-01-15 10:30:18 - Iniciando preprocesamiento...", class_="log-entry"),
                            ui.div("2024-01-15 10:30:19 - Aplicando diferenciación...", class_="log-entry"),
                            ui.div("2024-01-15 10:30:20 - Ajustando modelo ARIMA(1,1,1)...", class_="log-entry"),
                            ui.div("2024-01-15 10:30:25 - Modelo ajustado exitosamente", class_="log-entry"),
                            ui.div("2024-01-15 10:30:26 - Calculando métricas de validación...", class_="log-entry"),
                            ui.div("2024-01-15 10:30:30 - Análisis completado", class_="log-entry"),
                            class_="log-container"
                        ),
                        class_="log-wrapper"
                    ),
                    class_="mt-3"
                ),
                id="log_content",
                class_="d-none"
            )
        )
    )
    
    # Performance metrics section
    performance_section = create_card(
        title="⚡ Métricas de Rendimiento",
        subtitle="Estadísticas de ejecución y recursos",
        content=ui.div(
            ui.div(
                ui.div("📊", class_="file-upload-icon"),
                ui.div("Las métricas se mostrarán durante la ejecución", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Tiempo de ejecución:"),
                    ui.div(
                        ui.div("Tiempo total: 0:00:00", id="total_time"),
                        ui.div("Tiempo por modelo: 0:00:00", id="time_per_model"),
                        ui.div("Tiempo restante: 0:00:00", id="remaining_time"),
                        class_="mt-2"
                    ),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Uso de recursos:"),
                    ui.div(
                        ui.div("CPU: 0%", id="cpu_usage"),
                        ui.div("Memoria: 0 MB", id="memory_usage"),
                        ui.div("Procesos activos: 0", id="active_processes"),
                        class_="mt-2"
                    ),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Progreso por modelo:"),
                    ui.div(
                        ui.div("ARIMA(1,1,1): 0%", class_="model-progress"),
                        ui.div("SARIMA(1,1,1)(1,1,1,12): 0%", class_="model-progress"),
                        ui.div("ARIMA automático: 0%", class_="model-progress"),
                        class_="mt-2"
                    ),
                    class_="mt-3"
                ),
                id="performance_content",
                class_="d-none"
            )
        )
    )
    
    # Error handling section
    error_section = create_card(
        title="⚠️ Manejo de Errores",
        subtitle="Gestión de errores y recuperación",
        content=ui.div(
            ui.div(
                ui.div("✅", class_="file-upload-icon"),
                ui.div("No hay errores detectados", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Errores detectados:"),
                    ui.div(
                        ui.div("No hay errores", class_="status-indicator status-success"),
                        class_="mt-2"
                    ),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Configuración de recuperación:"),
                    ui.div(
                        ui.input_switch("auto_retry", "Reintento automático", value=True),
                        ui.input_numeric("max_retries", "Máximo de reintentos", value=3, min=1, max=10),
                        ui.input_switch("continue_on_error", "Continuar con errores", value=False),
                        class_="mt-2"
                    ),
                    class_="mt-3"
                ),
                id="error_content",
                class_="d-none"
            )
        )
    )
    
    return ui.div(
        control_section,
        progress_section,
        log_section,
        performance_section,
        error_section,
        class_="execution-container"
    )
