"""
Reusable UI components for TSLib Shiny App
Clean, professional design without emojis
"""

from shiny import ui
from htmltools import HTML, div, h3, h4, p, span, tags


def upload_card():
    """Card component for file upload"""
    return ui.card(
        ui.card_header(
            h3("Cargar Datos", class_="card-title"),
            p("Sube un archivo CSV o Excel, o selecciona un dataset de ejemplo", class_="card-subtitle")
        ),
        ui.div(
            # File upload
            ui.input_file(
                "file_upload",
                "Seleccionar archivo",
                accept=[".csv", ".xlsx", ".xls"],
                multiple=False
            ),
            
            # Example datasets
            ui.div(
                h4("Datos de Ejemplo", class_="mt-4 mb-3"),
                ui.div(
                    ui.input_action_button(
                        "load_airline",
                        "Pasajeros Aéreos",
                        class_="btn btn-outline-primary me-2 mb-2"
                    ),
                    ui.input_action_button(
                        "load_temperature", 
                        "Temperatura",
                        class_="btn btn-outline-primary me-2 mb-2"
                    ),
                    ui.input_action_button(
                        "load_sales",
                        "Ventas",
                        class_="btn btn-outline-primary me-2 mb-2"
                    ),
                    class_="d-flex flex-wrap"
                ),
                class_="mb-4"
            ),
            
            # Upload button
            ui.div(
                ui.input_action_button(
                    "upload_btn",
                    "Cargar Datos",
                    class_="btn btn-primary"
                ),
                class_="text-center"
            ),
            
            class_="card-body"
        ),
        class_="card"
    )


def stats_card(title, value, description=None):
    """Card component for displaying a single metric"""
    return ui.div(
        ui.div(
            ui.div(
                h3(f"{value}", class_="metric-value"),
                p(title, class_="metric-label"),
                p(description, class_="metric-description") if description else None,
                class_="text-center"
            ),
            class_="metric-card"
        ),
        class_="col-md-3 mb-3"
    )


def data_preview_card():
    """Card component for data preview table"""
    return ui.card(
        ui.card_header(
            h3("Vista Previa de Datos", class_="card-title"),
            p("Primeras filas del dataset cargado", class_="card-subtitle")
        ),
        ui.div(
            ui.output_data_frame("data_preview"),
            class_="data-table"
        ),
        class_="card"
    )


def time_series_plot_card():
    """Card component for time series visualization"""
    return ui.card(
        ui.card_header(
            h3("Serie Temporal", class_="card-title"),
            p("Visualización interactiva de los datos", class_="card-subtitle")
        ),
        ui.div(
            ui.output_plot("time_series_plot", height="400px"),
            class_="plot-container"
        ),
        class_="card"
    )


def model_config_card():
    """Card component for ARIMA model configuration"""
    return ui.card(
        ui.card_header(
            h3("Configuración del Modelo", class_="card-title"),
            p("Ajusta los parámetros ARIMA (p, d, q)", class_="card-subtitle")
        ),
        ui.div(
            # Mode selection
            ui.div(
                h4("Modo de Selección", class_="mb-3"),
                ui.input_radio_buttons(
                    "model_mode",
                    "Selecciona el modo:",
                    {
                        "auto": "Automático (recomendado)",
                        "manual": "Manual"
                    },
                    selected="auto"
                ),
                class_="mb-4"
            ),
            
            # Manual parameters (conditional)
            ui.div(
                h4("Parámetros Manuales", class_="mb-3"),
                ui.div(
                    ui.div(
                        ui.input_slider(
                            "param_p",
                            "p (AR - AutoRegresivo):",
                            min=0, max=5, value=1, step=1
                        ),
                        p("Orden del componente autorregresivo", class_="text-muted small"),
                        class_="mb-3"
                    ),
                    ui.div(
                        ui.input_slider(
                            "param_d", 
                            "d (I - Integración):",
                            min=0, max=2, value=1, step=1
                        ),
                        p("Orden de diferenciación", class_="text-muted small"),
                        class_="mb-3"
                    ),
                    ui.div(
                        ui.input_slider(
                            "param_q",
                            "q (MA - Media Móvil):",
                            min=0, max=5, value=1, step=1
                        ),
                        p("Orden del componente de media móvil", class_="text-muted small"),
                        class_="mb-3"
                    ),
                    id="manual_params"
                ),
                class_="mb-4"
            ),
            
            # Parallelization
            ui.div(
                h4("Paralelización", class_="mb-3"),
                ui.input_slider(
                    "n_jobs",
                    "Número de cores (n_jobs):",
                    min=1, max=8, value=4, step=1
                ),
                p("Usa más cores para acelerar el procesamiento", class_="text-muted small"),
                class_="mb-4"
            ),
            
            # Fit button
            ui.div(
                ui.input_action_button(
                    "fit_model_btn",
                    "Ajustar Modelo",
                    class_="btn btn-primary btn-lg"
                ),
                class_="text-center"
            ),
            
            class_="card-body"
        ),
        class_="card"
    )


def model_summary_card():
    """Card component for model summary and metrics"""
    return ui.card(
        ui.card_header(
            h3("Resumen del Modelo", class_="card-title"),
            p("Métricas y parámetros del modelo ajustado", class_="card-subtitle")
        ),
        ui.div(
            # Model info
            ui.div(
                stats_card("Modelo Seleccionado", "ARIMA(1,1,1)"),
                stats_card("AIC", "-245.67"),
                stats_card("BIC", "-238.45"),
                stats_card("Log-Likelihood", "125.33"),
                class_="row"
            ),
            
            # Parameters table
            ui.div(
                h4("Parámetros Estimados", class_="mt-4 mb-3"),
                ui.output_data_frame("model_params_table"),
                class_="data-table"
            ),
            
            class_="card-body"
        ),
        class_="card"
    )


def diagnostic_plots_card():
    """Card component for diagnostic plots grid"""
    return ui.card(
        ui.card_header(
            h3("Diagnósticos del Modelo", class_="card-title"),
            p("Análisis de residuos y bondad de ajuste", class_="card-subtitle")
        ),
        ui.div(
            ui.div(
                ui.div(
                    ui.div(
                        h4("Residuos vs Tiempo", class_="plot-title"),
                        ui.output_plot("residuals_plot", height="300px"),
                        class_="plot-container"
                    ),
                    class_="col-md-6 mb-3"
                ),
                ui.div(
                    ui.div(
                        h4("ACF de Residuos", class_="plot-title"),
                        ui.output_plot("acf_plot", height="300px"),
                        class_="plot-container"
                    ),
                    class_="col-md-6 mb-3"
                ),
                class_="row"
            ),
            ui.div(
                ui.div(
                    ui.div(
                        h4("Q-Q Plot", class_="plot-title"),
                        ui.output_plot("qq_plot", height="300px"),
                        class_="plot-container"
                    ),
                    class_="col-md-6 mb-3"
                ),
                ui.div(
                    ui.div(
                        h4("Histograma de Residuos", class_="plot-title"),
                        ui.output_plot("histogram_plot", height="300px"),
                        class_="plot-container"
                    ),
                    class_="col-md-6 mb-3"
                ),
                class_="row"
            ),
            class_="card-body"
        ),
        class_="card"
    )


def forecast_card():
    """Card component for forecasting"""
    return ui.card(
        ui.card_header(
            h3("Predicciones", class_="card-title"),
            p("Genera predicciones futuras con intervalos de confianza", class_="card-subtitle")
        ),
        ui.div(
            # Forecast controls
            ui.div(
                ui.div(
                    h4("Configuración de Predicción", class_="mb-3"),
                    ui.input_slider(
                        "forecast_steps",
                        "Pasos futuros:",
                        min=1, max=50, value=10, step=1
                    ),
                    p("Número de períodos a predecir", class_="text-muted small"),
                    class_="mb-4"
                ),
                class_="col-md-4"
            ),
            
            # Forecast plot
            ui.div(
                ui.div(
                    h4("Gráfico de Predicción", class_="plot-title"),
                    ui.output_plot("forecast_plot", height="400px"),
                    class_="plot-container"
                ),
                class_="col-md-8"
            ),
            
            class_="row"
        ),
        
        # Forecast table and download
        ui.div(
            ui.div(
                h4("Valores Predichos", class_="mb-3"),
                ui.output_data_frame("forecast_table"),
                class_="data-table mb-3"
            ),
            ui.div(
                ui.input_action_button(
                    "download_forecast",
                    "Descargar Predicciones",
                    class_="btn btn-success"
                ),
                class_="text-center"
            ),
            class_="card-body"
        ),
        class_="card"
    )


def step_indicator(current_step=1):
    """Step indicator component for navigation"""
    steps = [
        ("Datos", "Cargar datos"),
        ("Explorar", "Visualizar serie"),
        ("Configurar", "Parámetros modelo"),
        ("Ajustar", "Entrenar modelo"),
        ("Diagnosticar", "Análisis residuos"),
        ("Predecir", "Generar forecast")
    ]
    
    step_elements = []
    for i, (title, desc) in enumerate(steps, 1):
        step_class = "step"
        if i == current_step:
            step_class += " active"
        elif i < current_step:
            step_class += " completed"
            
        step_elements.append(
            ui.div(
                ui.div(
                    ui.div(
                        span(str(i), class_="step-number"),
                        ui.div(
                            h4(title, class_="mb-1"),
                            p(desc, class_="small text-muted mb-0"),
                            class_="d-inline-block"
                        ),
                        class_="d-flex align-items-center"
                    ),
                    class_=step_class
                ),
                class_="col-md-2 text-center"
            )
        )
    
    return ui.div(
        ui.div(
            *step_elements,
            class_="row"
        ),
        class_="step-indicator mb-4"
    )


def loading_spinner(text="Procesando..."):
    """Loading spinner component"""
    return ui.div(
        ui.div(
            ui.div(
                ui.div(
                    span("", class_="spinner me-2"),
                    span(text),
                    class_="d-flex align-items-center justify-content-center"
                ),
                class_="alert alert-info text-center"
            ),
            class_="col-md-6 offset-md-3"
        ),
        class_="row"
    )


def success_message(text="Operación completada exitosamente!"):
    """Success message component"""
    return ui.div(
        ui.div(
            ui.div(
                span("✓", class_="me-2"),
                span(text),
                class_="d-flex align-items-center"
            ),
            class_="alert alert-success"
        ),
        class_="col-md-8 offset-md-2"
    )


def error_message(text="Ha ocurrido un error. Por favor, inténtalo de nuevo."):
    """Error message component"""
    return ui.div(
        ui.div(
            ui.div(
                span("✗", class_="me-2"),
                span(text),
                class_="d-flex align-items-center"
            ),
            class_="alert alert-danger"
        ),
        class_="col-md-8 offset-md-2"
    )