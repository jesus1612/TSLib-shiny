# Results feature UI components
from shiny import ui
from components.layout import create_card, create_metric_card, create_data_table

def render_results_ui() -> ui.Tag:
    """Render results step UI components"""
    
    # Model comparison section
    comparison_section = create_card(
        title="📊 Comparación de Modelos",
        subtitle="Evaluación y ranking de modelos ajustados",
        content=ui.div(
            ui.div(
                ui.div("📈", class_="file-upload-icon"),
                ui.div("Los resultados se mostrarán después de la ejecución", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.div(
                        ui.input_action_button("refresh_results", "🔄 Actualizar Resultados", class_="btn btn-primary"),
                        ui.input_action_button("export_comparison", "💾 Exportar Comparación", class_="btn btn-secondary"),
                        class_="d-flex gap-2 mb-3"
                    ),
                    ui.div(
                        ui.div(
                            ui.h4("Ranking de modelos:"),
                            ui.div(
                                ui.div("1. ARIMA(1,1,1) - AIC: 1234.56", class_="model-ranking-item"),
                                ui.div("2. SARIMA(1,1,1)(1,1,1,12) - AIC: 1235.78", class_="model-ranking-item"),
                                ui.div("3. ARIMA(2,1,2) - AIC: 1236.90", class_="model-ranking-item"),
                                class_="ranking-list"
                            ),
                            class_="mb-3"
                        ),
                        ui.div(
                            ui.h4("Tabla comparativa:"),
                            ui.div(id="comparison_table"),
                            class_="mt-3"
                        ),
                        id="comparison_content"
                    ),
                    class_="mt-3"
                ),
                id="comparison_results",
                class_="d-none"
            )
        )
    )
    
    # Forecast visualization section
    forecast_section = create_card(
        title="🔮 Visualización de Predicciones",
        subtitle="Gráficos de pronósticos con intervalos de confianza",
        content=ui.div(
            ui.div(
                ui.div("📊", class_="file-upload-icon"),
                ui.div("Los gráficos de predicción se generarán automáticamente", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.div(
                        ui.input_action_button("generate_forecast", "🔮 Generar Predicciones", class_="btn btn-primary"),
                        ui.input_numeric("forecast_horizon", "Horizonte de predicción:", value=12, min=1, max=60),
                        ui.input_slider("confidence_level", "Nivel de confianza:", min=80, max=99, value=95),
                        class_="d-flex gap-2 mb-3"
                    ),
                    ui.div(
                        ui.div("Gráfico de predicciones", id="forecast_plot"),
                        class_="plot-container"
                    ),
                    class_="mt-3"
                ),
                id="forecast_content",
                class_="d-none"
            )
        )
    )
    
    # Model metrics section
    metrics_section = create_card(
        title="📏 Métricas de Evaluación",
        subtitle="Análisis detallado del rendimiento de los modelos",
        content=ui.div(
            ui.div(
                ui.div("📊", class_="file-upload-icon"),
                ui.div("Las métricas se calcularán automáticamente", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Criterios de información:"),
                    ui.div(
                        create_metric_card("1234.56", "AIC", "📊"),
                        create_metric_card("1256.78", "BIC", "📊"),
                        create_metric_card("1235.12", "AICC", "📊"),
                        create_metric_card("1245.34", "HQIC", "📊"),
                        class_="metrics-grid"
                    ),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Métricas de pronóstico:"),
                    ui.div(
                        create_metric_card("15.23", "RMSE", "📏"),
                        create_metric_card("12.45", "MAE", "📏"),
                        create_metric_card("8.67", "MAPE (%)", "📏"),
                        create_metric_card("85.5", "SMAPE (%)", "📏"),
                        class_="metrics-grid"
                    ),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Precisión direccional:"),
                    ui.div(
                        create_metric_card("78.5", "Accuracy (%)", "🎯"),
                        create_metric_card("82.3", "Precision (%)", "🎯"),
                        create_metric_card("75.8", "Recall (%)", "🎯"),
                        create_metric_card("79.0", "F1-Score (%)", "🎯"),
                        class_="metrics-grid"
                    ),
                    class_="mt-3"
                ),
                id="metrics_content",
                class_="d-none"
            )
        )
    )
    
    # Residual analysis section
    residual_section = create_card(
        title="🔍 Análisis de Residuos",
        subtitle="Diagnóstico de residuos y validación del modelo",
        content=ui.div(
            ui.div(
                ui.div("🔬", class_="file-upload-icon"),
                ui.div("El análisis de residuos se realizará automáticamente", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.div(
                        ui.input_action_button("analyze_residuals", "🔍 Analizar Residuos", class_="btn btn-primary"),
                        ui.input_select("residual_model", "Modelo a analizar:", 
                            choices={"arima": "ARIMA(1,1,1)", "sarima": "SARIMA(1,1,1)(1,1,1,12)"},
                            selected="arima"
                        ),
                        class_="d-flex gap-2 mb-3"
                    ),
                    ui.div(
                        ui.div("Gráfico de residuos", id="residual_plot"),
                        ui.div("Q-Q plot", id="qq_plot"),
                        ui.div("ACF de residuos", id="residual_acf"),
                        class_="plot-container"
                    ),
                    class_="mt-3"
                ),
                ui.div(
                    ui.h4("Tests diagnósticos:"),
                    ui.div(
                        ui.div("Ljung-Box: p-valor = 0.234 (No significativo)", class_="status-indicator status-success"),
                        ui.div("Shapiro-Wilk: p-valor = 0.156 (Normalidad)", class_="status-indicator status-success"),
                        ui.div("Breusch-Pagan: p-valor = 0.089 (Heterocedasticidad)", class_="status-indicator status-warning"),
                        class_="mt-2"
                    ),
                    class_="mt-3"
                ),
                id="residual_content",
                class_="d-none"
            )
        )
    )
    
    # Model details section
    details_section = create_card(
        title="📋 Detalles del Modelo",
        subtitle="Información técnica del modelo seleccionado",
        content=ui.div(
            ui.div(
                ui.div("📄", class_="file-upload-icon"),
                ui.div("Los detalles del modelo se mostrarán aquí", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Parámetros del modelo:"),
                    ui.div(
                        ui.div("AR(1): 0.456", class_="parameter-item"),
                        ui.div("MA(1): -0.234", class_="parameter-item"),
                        ui.div("Sigma²: 12.34", class_="parameter-item"),
                        class_="mt-2"
                    ),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Estadísticas del ajuste:"),
                    ui.div(
                        ui.div("Log-likelihood: -612.34", class_="stat-item"),
                        ui.div("AIC: 1234.56", class_="stat-item"),
                        ui.div("BIC: 1256.78", class_="stat-item"),
                        ui.div("Número de observaciones: 1000", class_="stat-item"),
                        class_="mt-2"
                    ),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Intervalos de confianza:"),
                    ui.div(
                        ui.div("AR(1): [0.234, 0.678]", class_="ci-item"),
                        ui.div("MA(1): [-0.456, -0.012]", class_="ci-item"),
                        ui.div("Sigma²: [10.12, 15.67]", class_="ci-item"),
                        class_="mt-2"
                    ),
                    class_="mt-3"
                ),
                id="details_content",
                class_="d-none"
            )
        )
    )
    
    # Export options section
    export_section = create_card(
        title="💾 Opciones de Exportación",
        subtitle="Descargar resultados y visualizaciones",
        content=ui.div(
            ui.div(
                ui.h4("Exportar datos:"),
                ui.div(
                    ui.input_action_button("export_forecast", "📊 Predicciones (CSV)", class_="btn btn-secondary"),
                    ui.input_action_button("export_metrics", "📏 Métricas (JSON)", class_="btn btn-secondary"),
                    ui.input_action_button("export_residuals", "🔍 Residuos (CSV)", class_="btn btn-secondary"),
                    class_="d-flex gap-2 mb-3"
                ),
                class_="mb-3"
            ),
            ui.div(
                ui.h4("Exportar gráficos:"),
                ui.div(
                    ui.input_action_button("export_forecast_plot", "📈 Gráfico de Predicciones (PNG)", class_="btn btn-secondary"),
                    ui.input_action_button("export_residual_plot", "🔍 Gráfico de Residuos (PNG)", class_="btn btn-secondary"),
                    ui.input_action_button("export_all_plots", "📊 Todos los Gráficos (ZIP)", class_="btn btn-secondary"),
                    class_="d-flex gap-2 mb-3"
                ),
                class_="mt-3"
            )
        )
    )
    
    return ui.div(
        comparison_section,
        forecast_section,
        metrics_section,
        residual_section,
        details_section,
        export_section,
        class_="results-container"
    )
