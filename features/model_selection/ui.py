# Model selection feature UI components
from shiny import ui
from components.layout import create_card, create_form_group, create_metric_card

def render_model_selection_ui() -> ui.Tag:
    """Render model selection step UI components"""
    
    # ARIMA parameters section
    arima_section = create_card(
        title="⚙️ Parámetros ARIMA",
        subtitle="Configuración de parámetros del modelo ARIMA",
        content=ui.div(
            ui.div(
                ui.div(
                    ui.input_switch("auto_arima", "Selección automática", value=True),
                    ui.p("Activar para selección automática de parámetros", class_="text-muted"),
                    class_="mb-3"
                ),
                ui.div(
                    ui.div(
                        create_form_group(
                            label="Orden AR (p)",
                            control=ui.input_numeric("ar_order", "Orden AR", value=1, min=0, max=10, class_="form-control"),
                            help_text="Número de términos autorregresivos"
                        ),
                        create_form_group(
                            label="Orden MA (q)",
                            control=ui.input_numeric("ma_order", "Orden MA", value=1, min=0, max=10, class_="form-control"),
                            help_text="Número de términos de media móvil"
                        ),
                        class_="col-md-6"
                    ),
                    ui.div(
                        create_form_group(
                            label="Diferenciación (d)",
                            control=ui.input_numeric("diff_order", "Orden de diferenciación", value=1, min=0, max=3, class_="form-control"),
                            help_text="Número de diferencias para estacionariedad"
                        ),
                        create_form_group(
                            label="Paralelización",
                            control=ui.input_slider("n_jobs", "Número de trabajos paralelos", min=1, max=8, value=4, class_="form-control"),
                            help_text="Número de procesos paralelos para optimización"
                        ),
                        class_="col-md-6"
                    ),
                    class_="row",
                    id="manual_params"
                ),
                ui.div(
                    ui.div(
                        ui.h4("Configuración automática:"),
                        ui.div(
                            ui.div("Rango AR: 0-5", class_="status-indicator status-info"),
                            ui.div("Rango MA: 0-5", class_="status-indicator status-info"),
                            ui.div("Diferenciación: Automática", class_="status-indicator status-info"),
                            class_="mt-2"
                        ),
                        class_="mt-3"
                    ),
                    id="auto_params"
                )
            )
        )
    )
    
    # Seasonal ARIMA section
    seasonal_section = create_card(
        title="🗓️ Modelo Estacional SARIMA",
        subtitle="Configuración de parámetros estacionales",
        content=ui.div(
            ui.div(
                ui.input_switch("use_seasonal", "Usar modelo estacional", value=False),
                ui.p("Activar para incluir componentes estacionales", class_="text-muted"),
                class_="mb-3"
            ),
            ui.div(
                ui.div(
                    create_form_group(
                        label="Período estacional",
                        control=ui.input_numeric("seasonal_period", "Período", value=12, min=2, max=24, class_="form-control"),
                        help_text="Período de la estacionalidad (ej: 12 para mensual)"
                    ),
                    create_form_group(
                        label="Orden AR estacional (P)",
                        control=ui.input_numeric("seasonal_ar", "AR estacional", value=1, min=0, max=3, class_="form-control"),
                        help_text="Términos AR estacionales"
                    ),
                    class_="col-md-6"
                ),
                ui.div(
                    create_form_group(
                        label="Orden MA estacional (Q)",
                        control=ui.input_numeric("seasonal_ma", "MA estacional", value=1, min=0, max=3, class_="form-control"),
                        help_text="Términos MA estacionales"
                    ),
                    create_form_group(
                        label="Diferenciación estacional (D)",
                        control=ui.input_numeric("seasonal_diff", "Dif. estacional", value=1, min=0, max=2, class_="form-control"),
                        help_text="Diferenciación estacional"
                    ),
                    class_="col-md-6"
                ),
                class_="row",
                id="seasonal_params"
            )
        )
    )
    
    # Model comparison section
    comparison_section = create_card(
        title="🔄 Comparación de Modelos",
        subtitle="Configuración para evaluación múltiple",
        content=ui.div(
            ui.div(
                ui.h4("Modelos a evaluar:"),
                ui.div(
                    ui.input_checkbox("compare_arima", "ARIMA básico", value=True),
                    ui.input_checkbox("compare_sarima", "SARIMA estacional", value=True),
                    ui.input_checkbox("compare_auto", "ARIMA automático", value=True),
                    ui.input_checkbox("compare_custom", "Modelo personalizado", value=False),
                    class_="mt-2"
                ),
                class_="mb-3"
            ),
            ui.div(
                ui.h4("Configuración de validación:"),
                ui.div(
                    create_form_group(
                        label="Método de validación",
                        control=ui.input_select("validation_method", "Método", 
                            choices={"holdout": "Holdout", "cv": "Validación cruzada", "walk_forward": "Walk-forward"},
                            selected="holdout",
                            class_="form-control"
                        )
                    ),
                    create_form_group(
                        label="Porcentaje de entrenamiento",
                        control=ui.input_slider("train_split", "Entrenamiento (%)", min=60, max=90, value=80, class_="form-control")
                    ),
                    class_="row"
                ),
                class_="mt-3"
            )
        )
    )
    
    # Advanced options section
    advanced_section = create_card(
        title="🔧 Opciones Avanzadas",
        subtitle="Configuraciones adicionales para el modelado",
        content=ui.div(
            ui.div(
                ui.h4("Optimización:"),
                ui.div(
                    create_form_group(
                        label="Algoritmo de optimización",
                        control=ui.input_select("optimizer", "Optimizador",
                            choices={"lbfgs": "L-BFGS", "bfgs": "BFGS", "powell": "Powell", "cg": "Conjugate Gradient"},
                            selected="lbfgs",
                            class_="form-control"
                        )
                    ),
                    create_form_group(
                        label="Máximo de iteraciones",
                        control=ui.input_numeric("max_iter", "Iteraciones", value=1000, min=100, max=5000, class_="form-control")
                    ),
                    class_="row"
                ),
                class_="mb-3"
            ),
            ui.div(
                ui.h4("Criterios de información:"),
                ui.div(
                    ui.input_checkbox("use_aic", "AIC", value=True),
                    ui.input_checkbox("use_bic", "BIC", value=True),
                    ui.input_checkbox("use_aicc", "AICC", value=True),
                    ui.input_checkbox("use_hqic", "HQIC", value=False),
                    class_="mt-2"
                ),
                class_="mb-3"
            ),
            ui.div(
                ui.h4("Configuración de Spark (opcional):"),
                ui.div(
                    ui.input_switch("use_spark", "Usar PySpark", value=False),
                    ui.p("Activar para procesamiento distribuido", class_="text-muted"),
                    class_="mb-2"
                ),
                ui.div(
                    create_form_group(
                        label="Número de particiones",
                        control=ui.input_numeric("spark_partitions", "Particiones", value=4, min=2, max=16, class_="form-control")
                    ),
                    id="spark_config",
                    class_="d-none"
                )
            )
        )
    )
    
    # Model summary section
    summary_section = create_card(
        title="📋 Resumen de Configuración",
        subtitle="Vista previa de la configuración seleccionada",
        content=ui.div(
            ui.div(
                ui.div("⚙️", class_="file-upload-icon"),
                ui.div("La configuración se mostrará aquí", class_="file-upload-text"),
                class_="file-upload-area"
            ),
            ui.div(
                ui.div(
                    ui.h4("Modelo principal:"),
                    ui.div("ARIMA(1,1,1)", id="main_model"),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Modelos adicionales:"),
                    ui.div(
                        ui.div("SARIMA(1,1,1)(1,1,1,12)", class_="status-indicator status-info"),
                        ui.div("ARIMA automático", class_="status-indicator status-info"),
                        class_="mt-2"
                    ),
                    class_="mb-3"
                ),
                ui.div(
                    ui.h4("Configuración:"),
                    ui.div(
                        create_metric_card("4", "Procesos paralelos", "⚡"),
                        create_metric_card("80%", "Entrenamiento", "📊"),
                        create_metric_card("L-BFGS", "Optimizador", "🔧"),
                        create_metric_card("1000", "Max iteraciones", "🔄"),
                        class_="metrics-grid"
                    ),
                    class_="mt-3"
                ),
                id="config_summary",
                class_="d-none"
            )
        )
    )
    
    return ui.div(
        arima_section,
        seasonal_section,
        comparison_section,
        advanced_section,
        summary_section,
        class_="model-selection-container"
    )
