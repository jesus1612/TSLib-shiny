"""
Layout components for TSLib Shiny App
"""

from shiny import ui
from htmltools import HTML, div, h1, h2, h3, h4, p, span, tags
from .components import (
    upload_card, stats_card, data_preview_card, time_series_plot_card,
    model_config_card, model_summary_card, diagnostic_plots_card,
    forecast_card, step_indicator
)


def create_header():
    """Header component with app title and description"""
    return ui.div(
        ui.div(
            ui.div(
                h1("TSLib Shiny App", class_="display-4 fw-bold text-primary mb-2"),
                p(
                    "Análisis profesional de series temporales con modelos ARIMA",
                    class_="lead text-muted mb-0"
                ),
                class_="text-center header-section"
            ),
            class_="col-12"
        ),
        class_="row mb-5"
    )


def create_sidebar():
    """Sidebar component with navigation and app info"""
    return ui.sidebar(
        # App info
        ui.div(
            h2("TSLib", class_="sidebar-title"),
            p("Time Series Library", class_="sidebar-subtitle"),
            class_="sidebar-header"
        ),
        
        # Navigation
        ui.div(
            h3("Navegación", class_="h5 mb-3"),
            ui.div(
                ui.div("📁 Datos", class_="nav-item mb-2"),
                ui.div("📊 Explorar", class_="nav-item mb-2"),
                ui.div("⚙️ Configurar", class_="nav-item mb-2"),
                ui.div("🚀 Ajustar", class_="nav-item mb-2"),
                ui.div("🔍 Diagnosticar", class_="nav-item mb-2"),
                ui.div("🔮 Predecir", class_="nav-item mb-2"),
                class_="nav-pills flex-column"
            ),
            class_="mb-4"
        ),
        
        # Current step info
        ui.div(
            h3("Paso Actual", class_="h5 mb-3"),
            ui.div(
                ui.div(
                    span("📁", class_="fs-4 me-2"),
                    ui.div(
                        h4("Cargar Datos", class_="mb-1"),
                        p("Sube tu archivo CSV o Excel", class_="small text-muted mb-0"),
                        class_="d-inline-block"
                    ),
                    class_="d-flex align-items-center p-3 bg-light rounded"
                ),
                id="current_step_info"
            ),
            class_="mb-4"
        ),
        
        # Help section
        ui.div(
            h3("Ayuda", class_="h5 mb-3"),
            ui.div(
                ui.div(
                    span("💡", class_="me-2"),
                    span("Usa los datos de ejemplo para probar la app"),
                    class_="small text-muted"
                ),
                class_="mb-2"
            ),
            ui.div(
                ui.div(
                    span("⚡", class_="me-2"),
                    span("Ajusta n_jobs para acelerar el procesamiento"),
                    class_="small text-muted"
                ),
                class_="mb-2"
            ),
            ui.div(
                ui.div(
                    span("📈", class_="me-2"),
                    span("Revisa los diagnósticos antes de predecir"),
                    class_="small text-muted"
                ),
                class_="mb-2"
            ),
            class_="p-3 bg-light rounded"
        ),
        
        title="TSLib App"
    )


def create_main_panel():
    """Main panel component with dynamic content"""
    return ui.div(
        ui.div(
            # Step indicator
            ui.div(
                step_indicator(current_step=1),
                id="step_indicator_container"
            ),
            
            # Main content area
            ui.div(
                # Step 1: Data Upload
                ui.div(
                    ui.div(
                        upload_card(),
                        class_="col-12 mb-4"
                    ),
                    ui.div(
                        data_preview_card(),
                        class_="col-12 mb-4"
                    ),
                    id="step1_content",
                    class_="row"
                ),
                
                # Step 2: Data Exploration
                ui.div(
                    ui.div(
                        time_series_plot_card(),
                        class_="col-12 mb-4"
                    ),
                    ui.div(
                        stats_card("Observaciones", "144", "Total de puntos"),
                        stats_card("Media", "280.3", "Valor promedio"),
                        stats_card("Desv. Est.", "119.7", "Variabilidad"),
                        stats_card("Rango", "112-622", "Min-Max"),
                        class_="row"
                    ),
                    id="step2_content",
                    class_="row d-none"
                ),
                
                # Step 3: Model Configuration
                ui.div(
                    ui.div(
                        model_config_card(),
                        class_="col-12 mb-4"
                    ),
                    id="step3_content",
                    class_="row d-none"
                ),
                
                # Step 4: Model Fitting
                ui.div(
                    ui.div(
                        model_summary_card(),
                        class_="col-12 mb-4"
                    ),
                    id="step4_content",
                    class_="row d-none"
                ),
                
                # Step 5: Diagnostics
                ui.div(
                    ui.div(
                        diagnostic_plots_card(),
                        class_="col-12 mb-4"
                    ),
                    id="step5_content",
                    class_="row d-none"
                ),
                
                # Step 6: Forecasting
                ui.div(
                    ui.div(
                        forecast_card(),
                        class_="col-12 mb-4"
                    ),
                    id="step6_content",
                    class_="row d-none"
                ),
                
                id="main_content"
            ),
            
            class_="container-fluid"
        ),
        id="main",
        class_="main-content"
    )


def create_app_ui():
    """Complete app UI layout"""
    return ui.page_fluid(
        # Include custom CSS
        ui.tags.head(
            ui.tags.link(
                rel="stylesheet",
                href="custom.css"
            ),
            ui.tags.meta(
                name="viewport",
                content="width=device-width, initial-scale=1"
            ),
            ui.tags.title("TSLib Shiny App - Análisis de Series Temporales")
        ),
        
        # Header
        create_header(),
        
        # Main content
        create_main_panel(),
        
        # Footer
        ui.div(
            ui.div(
                ui.div(
                    p(
                        "Desarrollado con ❤️ usando ",
                        ui.tags.a("Shiny for Python", href="https://shiny.posit.co/py/", target="_blank"),
                        " y ",
                        ui.tags.a("TSLib", href="#", target="_blank"),
                        class_="text-muted small mb-0"
                    ),
                    class_="text-center"
                ),
                class_="col-12"
            ),
            class_="row mt-5 pt-4 border-top"
        )
    )


def create_step_navigation():
    """Navigation component for moving between steps"""
    return ui.div(
        ui.div(
            ui.input_action_button(
                "prev_step",
                "⬅️ Anterior",
                class_="btn btn-outline-secondary me-2"
            ),
            ui.input_action_button(
                "next_step", 
                "Siguiente ➡️",
                class_="btn btn-primary"
            ),
            class_="d-flex justify-content-between"
        ),
        class_="row mt-4"
    )


def create_progress_bar(step, total_steps=6):
    """Progress bar component"""
    progress_percentage = (step / total_steps) * 100
    
    return ui.div(
        ui.div(
            ui.div(
                ui.div(
                    f"Paso {step} de {total_steps}",
                    class_="small text-muted"
                ),
                ui.div(
                    ui.div(
                        "",
                        class_="progress-bar",
                        style=f"width: {progress_percentage}%"
                    ),
                    class_="progress mt-2"
                ),
                class_="w-100"
            ),
            class_="col-12"
        ),
        class_="row mb-4"
    )