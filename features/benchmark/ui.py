# Benchmark feature UI components
from shiny import ui
from components.layout import create_card, create_form_group

def render_benchmark_ui() -> ui.Tag:
    """Render benchmark UI components"""
    
    return ui.div(
        ui.tags.h3("🚀 Benchmark de Rendimiento", class_="mb-4", style="color: var(--accent-primary);"),
        ui.tags.p(
            "Compara el tiempo de ajuste secuencial vs paralelo para distintos modelos y tamaños de serie.",
            class_="text-muted mb-4"
        ),
        
        ui.div(
            # Config panel
            ui.div(
                create_card(
                    title="Configuración",
                    subtitle="Parámetros del benchmark",
                    content=ui.div(
                        create_form_group(
                            label="Tamaños de serie (n_obs)",
                            control=ui.input_text(
                                "bench_n_obs",
                                "",
                                value="100, 500, 1000, 5000"
                            ),
                            help_text="Separados por comas (ej. 100, 500, 1000)"
                        ),
                        create_form_group(
                            label="Repeticiones por tamaño",
                            control=ui.input_numeric("bench_repeats", "", value=3, min=1, max=10),
                            help_text="Número de veces a ejecutar para tomar el menor tiempo"
                        ),
                        ui.div(
                            ui.input_action_button("run_benchmark", "▶️ Ejecutar Benchmark", class_="btn btn-primary btn-lg w-100 mt-4"),
                            class_="text-center"
                        ),
                        ui.output_ui("bench_execution_status")
                    )
                ),
                class_="col-md-4 mb-4"
            ),
            
            # Results panel
            ui.div(
                create_card(
                    title="Resultados",
                    subtitle="Comparativa de tiempos de ejecución",
                    content=ui.div(
                        ui.output_ui("bench_results_ui")
                    )
                ),
                class_="col-md-8"
            ),
            class_="row"
        )
    )
