# Reports feature UI components
from shiny import ui
from components.layout import create_card, create_form_group, create_action_buttons

def render_reports_ui() -> ui.Tag:
    """Render reports step UI components"""
    
    # Report configuration section
    config_section = create_card(
        title="⚙️ Configuración del Reporte",
        subtitle="Personalizar el contenido y formato del reporte",
        content=ui.div(
            ui.div(
                ui.h4("Contenido del reporte:"),
                ui.div(
                    ui.input_checkbox("include_summary", "Resumen ejecutivo", value=True),
                    ui.input_checkbox("include_data_info", "Información de datos", value=True),
                    ui.input_checkbox("include_visualizations", "Visualizaciones", value=True),
                    ui.input_checkbox("include_model_details", "Detalles del modelo", value=True),
                    ui.input_checkbox("include_forecasts", "Predicciones", value=True),
                    ui.input_checkbox("include_metrics", "Métricas de evaluación", value=True),
                    ui.input_checkbox("include_residuals", "Análisis de residuos", value=True),
                    ui.input_checkbox("include_recommendations", "Recomendaciones", value=True),
                    class_="mt-2"
                ),
                class_="mb-3"
            ),
            ui.div(
                ui.h4("Formato y estilo:"),
                ui.div(
                    create_form_group(
                        label="Formato de salida",
                        control=ui.input_select("report_format", "Formato",
                            choices={"pdf": "PDF", "html": "HTML", "docx": "Word", "md": "Markdown"},
                            selected="pdf",
                            class_="form-control"
                        )
                    ),
                    create_form_group(
                        label="Idioma",
                        control=ui.input_select("report_language", "Idioma",
                            choices={"es": "Español", "en": "English"},
                            selected="es",
                            class_="form-control"
                        )
                    ),
                    create_form_group(
                        label="Tema visual",
                        control=ui.input_select("report_theme", "Tema",
                            choices={"dark": "Oscuro", "light": "Claro", "professional": "Profesional"},
                            selected="professional",
                            class_="form-control"
                        )
                    ),
                    class_="row"
                ),
                class_="mt-3"
            )
        )
    )
    
    # Executive summary section
    summary_section = create_card(
        title="📋 Resumen Ejecutivo",
        subtitle="Vista previa del resumen ejecutivo",
        content=ui.div(
            ui.div(
                ui.div("📄", class_="file-upload-icon"),
                ui.div("El resumen se generará automáticamente", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Resumen del análisis:"),
                    ui.div(
                        ui.p("Se analizó una serie temporal de 1000 observaciones utilizando modelos ARIMA y SARIMA. El modelo ARIMA(1,1,1) mostró el mejor rendimiento con un AIC de 1234.56."),
                        ui.p("Las predicciones indican una tendencia estable con variabilidad estacional moderada. El modelo presenta residuos bien comportados sin autocorrelación significativa."),
                        ui.p("Se recomienda utilizar el modelo ARIMA(1,1,1) para predicciones a corto plazo (1-12 períodos) con intervalos de confianza del 95%."),
                        class_="summary-content"
                    ),
                    class_="mt-3"
                ),
                ui.div(
                    ui.h4("Conclusiones clave:"),
                    ui.div(
                        ui.div("✓ Modelo ARIMA(1,1,1) seleccionado como óptimo", class_="conclusion-item"),
                        ui.div("✓ RMSE de 15.23 en validación", class_="conclusion-item"),
                        ui.div("✓ Precisión direccional del 78.5%", class_="conclusion-item"),
                        ui.div("✓ Residuos cumplen supuestos del modelo", class_="conclusion-item"),
                        class_="mt-2"
                    ),
                    class_="mt-3"
                ),
                id="summary_content",
                class_="d-none"
            )
        )
    )
    
    # Technical report section
    technical_section = create_card(
        title="🔬 Reporte Técnico",
        subtitle="Documentación técnica detallada",
        content=ui.div(
            ui.div(
                ui.div("🔬", class_="file-upload-icon"),
                ui.div("El reporte técnico se generará automáticamente", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Metodología:"),
                    ui.div(
                        ui.p("Se utilizó el método de máxima verosimilitud para estimar los parámetros del modelo ARIMA. La selección del modelo se basó en criterios de información (AIC, BIC) y validación cruzada."),
                        ui.p("Los tests de estacionariedad (ADF, KPSS) confirmaron la necesidad de diferenciación. El análisis ACF/PACF guió la selección de órdenes AR y MA."),
                        class_="methodology-content"
                    ),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Resultados técnicos:"),
                    ui.div(
                        ui.div("Parámetros estimados:", class_="subtitle"),
                        ui.div("• AR(1): 0.456 (SE: 0.089)", class_="result-item"),
                        ui.div("• MA(1): -0.234 (SE: 0.092)", class_="result-item"),
                        ui.div("• Sigma²: 12.34 (SE: 1.23)", class_="result-item"),
                        class_="mt-2"
                    ),
                    ui.div(
                        ui.div("Tests diagnósticos:", class_="subtitle"),
                        ui.div("• Ljung-Box: χ² = 15.23, p = 0.234", class_="result-item"),
                        ui.div("• Shapiro-Wilk: W = 0.987, p = 0.156", class_="result-item"),
                        ui.div("• Breusch-Pagan: χ² = 8.45, p = 0.089", class_="result-item"),
                        class_="mt-2"
                    ),
                    class_="mt-3"
                ),
                id="technical_content",
                class_="d-none"
            )
        )
    )
    
    # Recommendations section
    recommendations_section = create_card(
        title="💡 Recomendaciones",
        subtitle="Sugerencias para el uso del modelo",
        content=ui.div(
            ui.div(
                ui.div("💡", class_="file-upload-icon"),
                ui.div("Las recomendaciones se generarán automáticamente", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Uso del modelo:"),
                    ui.div(
                        ui.div("• Utilizar para predicciones a corto plazo (1-12 períodos)", class_="recommendation-item"),
                        ui.div("• Recalibrar mensualmente con nuevos datos", class_="recommendation-item"),
                        ui.div("• Monitorear métricas de rendimiento continuamente", class_="recommendation-item"),
                        ui.div("• Considerar modelos alternativos si el rendimiento decae", class_="recommendation-item"),
                        class_="mt-2"
                    ),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Limitaciones:"),
                    ui.div(
                        ui.div("• No captura cambios estructurales abruptos", class_="limitation-item"),
                        ui.div("• Rendimiento puede degradarse en horizontes largos", class_="limitation-item"),
                        ui.div("• Requiere datos estacionarios para funcionar óptimamente", class_="limitation-item"),
                        class_="mt-2"
                    ),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Próximos pasos:"),
                    ui.div(
                        ui.div("• Implementar monitoreo automático del modelo", class_="next-step-item"),
                        ui.div("• Evaluar modelos de machine learning como alternativa", class_="next-step-item"),
                        ui.div("• Considerar modelos multivariados si hay variables adicionales", class_="next-step-item"),
                        class_="mt-2"
                    ),
                    class_="mt-3"
                ),
                id="recommendations_content",
                class_="d-none"
            )
        )
    )
    
    # Report generation section
    generation_section = create_card(
        title="🚀 Generación de Reportes",
        subtitle="Crear y descargar reportes personalizados",
        content=ui.div(
            ui.div(
                ui.div(
                    ui.input_action_button("generate_report", "📄 Generar Reporte Completo", class_="btn btn-primary btn-lg"),
                    ui.input_action_button("preview_report", "👁️ Vista Previa", class_="btn btn-secondary"),
                    class_="d-flex gap-2 mb-3"
                ),
                ui.div(
                    ui.div("Estado: Listo para generar", id="report_status", class_="status-indicator status-info"),
                    ui.div("Tiempo estimado: 30-60 segundos", id="report_time", class_="text-muted"),
                    class_="mt-2"
                )
            ),
            ui.div(
                ui.div(
                    ui.h4("Progreso de generación:"),
                    ui.div(
                        ui.div("Preparando contenido...", class_="generation-step"),
                        ui.div("Generando visualizaciones...", class_="generation-step"),
                        ui.div("Compilando reporte...", class_="generation-step"),
                        ui.div("Finalizando...", class_="generation-step"),
                        class_="generation-steps"
                    ),
                    class_="mt-3"
                ),
                id="generation_progress",
                class_="d-none"
            )
        )
    )
    
    # Download section
    download_section = create_card(
        title="💾 Descarga de Reportes",
        subtitle="Acceder a reportes generados",
        content=ui.div(
            ui.div(
                ui.div("📁", class_="file-upload-icon"),
                ui.div("Los reportes generados aparecerán aquí", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Reportes disponibles:"),
                    ui.div(
                        ui.div(
                            ui.div("📄 Reporte_Completo_2024-01-15.pdf", class_="file-name"),
                            ui.div("2.3 MB • Generado hace 5 minutos", class_="file-info"),
                            ui.div(
                                ui.input_action_button("download_pdf", "📥 Descargar PDF", class_="btn btn-primary"),
                                ui.input_action_button("preview_pdf", "👁️ Vista Previa", class_="btn btn-secondary"),
                                class_="file-actions"
                            ),
                            class_="file-item"
                        ),
                        ui.div(
                            ui.div("📊 Datos_Procesados_2024-01-15.xlsx", class_="file-name"),
                            ui.div("1.8 MB • Generado hace 3 minutos", class_="file-info"),
                            ui.div(
                                ui.input_action_button("download_excel", "📥 Descargar Excel", class_="btn btn-primary"),
                                ui.input_action_button("preview_excel", "👁️ Vista Previa", class_="btn btn-secondary"),
                                class_="file-actions"
                            ),
                            class_="file-item"
                        ),
                        class_="files-list"
                    ),
                    class_="mt-3"
                ),
                ui.div(
                    ui.h4("Historial de reportes:"),
                    ui.div(
                        ui.div("📄 Reporte_2024-01-14.pdf • 1.9 MB", class_="history-item"),
                        ui.div("📄 Reporte_2024-01-13.pdf • 2.1 MB", class_="history-item"),
                        ui.div("📄 Reporte_2024-01-12.pdf • 1.7 MB", class_="history-item"),
                        class_="history-list"
                    ),
                    class_="mt-3"
                ),
                id="download_content",
                class_="d-none"
            )
        )
    )
    
    return ui.div(
        config_section,
        summary_section,
        technical_section,
        recommendations_section,
        generation_section,
        download_section,
        class_="reports-container"
    )
