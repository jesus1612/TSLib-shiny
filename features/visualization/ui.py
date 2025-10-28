# Visualization feature UI components
from shiny import ui
from components.layout import create_card, create_metric_card, create_form_group

def render_visualization_ui() -> ui.Tag:
    """Render visualization step UI components"""
    
    # Time series plot section
    plot_section = create_card(
        title="📈 Visualización de Serie Temporal",
        subtitle="Gráfico interactivo de la serie de tiempo",
        content=ui.div(
            ui.div(
                ui.div("📊", class_="file-upload-icon"),
                ui.div("El gráfico se generará después de cargar los datos", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
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
                id="plot_content",
                class_="d-none"
            )
        )
    )
    
    # Descriptive statistics section
    stats_section = create_card(
        title="📊 Estadísticas Descriptivas",
        subtitle="Análisis estadístico básico de la serie",
        content=ui.div(
            ui.div(
                ui.div("📈", class_="file-upload-icon"),
                ui.div("Las estadísticas se calcularán automáticamente", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Estadísticas básicas:"),
                    ui.div(
                        create_metric_card("0", "Media", "📊"),
                        create_metric_card("0", "Desv. Estándar", "📏"),
                        create_metric_card("0", "Asimetría", "📐"),
                        create_metric_card("0", "Curtosis", "📊"),
                        class_="metrics-grid"
                    ),
                    class_="mt-3"
                ),
                ui.div(
                    ui.h4("Rango de valores:"),
                    ui.div(
                        create_metric_card("0", "Mínimo", "⬇️"),
                        create_metric_card("0", "Máximo", "⬆️"),
                        create_metric_card("0", "Rango", "📏"),
                        create_metric_card("0", "Mediana", "📊"),
                        class_="metrics-grid"
                    ),
                    class_="mt-3"
                ),
                id="stats_content",
                class_="d-none"
            )
        )
    )
    
    # Stationarity tests section
    stationarity_section = create_card(
        title="🔍 Tests de Estacionariedad",
        subtitle="Verificación de propiedades estacionarias",
        content=ui.div(
            ui.div(
                ui.div("🔬", class_="file-upload-icon"),
                ui.div("Los tests se ejecutarán automáticamente", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Test de Dickey-Fuller Aumentado (ADF):"),
                    ui.div(
                        ui.div("Estadístico: 0.000", id="adf_statistic"),
                        ui.div("p-valor: 0.000", id="adf_pvalue"),
                        ui.div("Valores críticos:", id="adf_critical"),
                        ui.div("Resultado: Serie no estacionaria", id="adf_result", class_="status-indicator status-warning"),
                        class_="mt-2"
                    ),
                    class_="mt-3"
                ),
                ui.div(
                    ui.h4("Test de KPSS:"),
                    ui.div(
                        ui.div("Estadístico: 0.000", id="kpss_statistic"),
                        ui.div("p-valor: 0.000", id="kpss_pvalue"),
                        ui.div("Valores críticos:", id="kpss_critical"),
                        ui.div("Resultado: Serie no estacionaria", id="kpss_result", class_="status-indicator status-warning"),
                        class_="mt-2"
                    ),
                    class_="mt-3"
                ),
                id="stationarity_content",
                class_="d-none"
            )
        )
    )
    
    # ACF/PACF plots section
    acf_section = create_card(
        title="🔄 Análisis de Autocorrelación",
        subtitle="Gráficos ACF y PACF para identificación de modelo",
        content=ui.div(
            ui.div(
                ui.div("📊", class_="file-upload-icon"),
                ui.div("Los gráficos ACF/PACF se generarán automáticamente", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.div(
                        ui.input_action_button("generate_acf", "🔄 Generar ACF/PACF", class_="btn btn-primary"),
                        ui.input_numeric("acf_lags", "Número de lags:", value=20, min=5, max=50, class_="form-control"),
                        class_="d-flex gap-2 mb-3"
                    ),
                    ui.div(
                        ui.div("Gráfico ACF", id="acf_plot"),
                        ui.div("Gráfico PACF", id="pacf_plot"),
                        class_="plot-container"
                    ),
                    class_="mt-3"
                ),
                id="acf_content",
                class_="d-none"
            )
        )
    )
    
    # Seasonal analysis section
    seasonal_section = create_card(
        title="🗓️ Análisis Estacional",
        subtitle="Detección de patrones estacionales",
        content=ui.div(
            ui.div(
                ui.div("📅", class_="file-upload-icon"),
                ui.div("El análisis estacional se realizará automáticamente", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Detección de estacionalidad:"),
                    ui.div(
                        ui.div("Período detectado: 12", id="seasonal_period"),
                        ui.div("Fuerza estacional: 0.85", id="seasonal_strength"),
                        ui.div("Componente estacional: Detectado", id="seasonal_component", class_="status-indicator status-success"),
                        class_="mt-2"
                    ),
                    class_="mt-3"
                ),
                ui.div(
                    ui.h4("Descomposición estacional:"),
                    ui.div("Gráfico de descomposición", id="seasonal_decomposition"),
                    class_="mt-3"
                ),
                id="seasonal_content",
                class_="d-none"
            )
        )
    )
    
    return ui.div(
        plot_section,
        stats_section,
        stationarity_section,
        acf_section,
        seasonal_section,
        class_="visualization-container"
    )
