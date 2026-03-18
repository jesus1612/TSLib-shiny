# Benchmark feature server logic
from shiny import ui, reactive, render
from services.tslib_service import TSLibService
import matplotlib
import matplotlib.pyplot as plt
import io
import time
import os
import io

try:
    from tests.test_benchmark_parallelism import BenchmarkRunner
    BENCHMARK_AVAILABLE = True
except ImportError:
    BENCHMARK_AVAILABLE = False


def register_benchmark_server(input, output, session, app_state):
    """Register benchmark server functions"""
    
    # Render execution status
    @output
    @render.ui
    def bench_execution_status():
        state = app_state.get()
        if not BENCHMARK_AVAILABLE:
            return ui.div(
                ui.tags.p("⚠️ La suite de benchmark no está disponible.", class_="text-danger mt-3")
            )
            
        status = state.get("bench_status", "idle")
        if status == "running":
            return ui.div(
                ui.tags.div(class_="spinner-border text-primary", role="status"),
                ui.tags.span(" Ejecutando benchmark... esto puede tomar varios minutos.", class_="ms-2"),
                class_="mt-3 text-center"
            )
        elif status == "error":
            error_msg = state.get("bench_error", "Error desconocido")
            return ui.div(
                ui.tags.p(f"❌ Error: {error_msg}", class_="text-danger mt-3")
            )
        elif status == "done":
            return ui.div(
                ui.tags.p("✅ Benchmark completado con éxito.", class_="text-success mt-3")
            )
        
        return ui.div()
    
    # Main execution handler
    @reactive.Effect
    @reactive.event(input.run_benchmark)
    def handle_run_benchmark():
        """Run the actual benchmark asynchronously-like"""
        if not BENCHMARK_AVAILABLE:
            return
            
        # Parse inputs
        try:
            n_obs_str = input.bench_n_obs()
            n_obs_grid = [int(n.strip()) for n in n_obs_str.split(',') if n.strip()]
            if not n_obs_grid:
                raise ValueError("Se requiere al menos un tamaño de serie")
                
            repeats = int(input.bench_repeats())
            if repeats < 1:
                repeats = 1
        except Exception as e:
            new_state = app_state.get().copy()
            new_state["bench_status"] = "error"
            new_state["bench_error"] = str(e)
            app_state.set(new_state)
            return
            
        # Set running state
        new_state = app_state.get().copy()
        new_state["bench_status"] = "running"
        app_state.set(new_state)
        
        # Give UI a moment to update
        
        try:
            # Create a silent version of the runner that doesn't print to stdout
            runner = BenchmarkRunner(n_obs_grid=n_obs_grid, repeats=repeats, seed=42)
            
            # Instead of a simple `run`, we mock out prints or just let it run
            # But redirect stdout to avoid clutter
            import contextlib
            with contextlib.redirect_stdout(io.StringIO()):
                runner.run()
            
            # Save results to state
            results = {
                "results": runner.results,
                "elbows": runner.elbow_threshold(),
                "n_obs_grid": runner.n_obs_grid,
                "models": runner.models
            }
            
            # Generate the plot
            fig = _create_elbow_plot(runner)
            
            new_state = app_state.get().copy()
            new_state["bench_status"] = "done"
            new_state["bench_results"] = results
            new_state["bench_plot"] = fig
            app_state.set(new_state)
            
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            new_state = app_state.get().copy()
            new_state["bench_status"] = "error"
            new_state["bench_error"] = str(e)
            print(error_msg)
            app_state.set(new_state)

    @output
    @render.ui
    def bench_results_ui():
        """Render the results block"""
        state = app_state.get()
        status = state.get("bench_status", "idle")
        results = state.get("bench_results", None)
        
        if status == "idle":
            return ui.div(
                ui.tags.p("Configura los parámetros y haz clic en Ejecutar.", class_="text-center text-muted p-5")
            )
            
        if status == "running":
            return ui.div(
                ui.tags.div(class_="spinner-grow text-primary mt-5", role="status", style="width: 3rem; height: 3rem;"),
                ui.tags.h5("Ejecutando modelado paralelo y secuencial..."),
                ui.tags.p("Esto tomará un tiempo dependiendo de los tamaños elegidos.", class_="text-muted"),
                class_="text-center p-5"
            )
            
        if status == "error":
            return ui.div(
                ui.tags.p("Ocurrió un error al ejecutar el benchmark.", class_="text-center text-danger p-5")
            )
            
        if status == "done" and results:
            return ui.div(
                ui.output_plot("bench_elbow_plot", height="800px"),
                ui.tags.h5("Resumen de 'Codos' (Speedup >= 1.1x)", class_="mt-4"),
                ui.output_ui("bench_summary_cards")
            )
            
        return ui.div()
        
    @output
    @render.plot
    def bench_elbow_plot():
        state = app_state.get()
        fig = state.get("bench_plot")
        if fig:
            return fig
        # Fallback
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "Sin datos de gráfico", ha="center")
        return fig
        
    @output
    @render.ui
    def bench_summary_cards():
        state = app_state.get()
        results = state.get("bench_results")
        if not results:
            return ui.div()
            
        elbows = results.get("elbows", {})
        
        cards = []
        for model_name, threshold in elbows.items():
            threshold_text = f"N >= {threshold}" if threshold is not None else "Pierde paralelo"
            icon = "📈" if threshold is not None else "📉"
            status_class = "border-success" if threshold is not None else "border-warning"
            
            cards.append(
                ui.div(
                    ui.div(
                        ui.div(icon, class_="metric-icon"),
                        ui.div(model_name, class_="metric-label fw-bold"),
                        ui.div(threshold_text, class_="metric-value", style="font-size: 1.2rem;"),
                        class_="metric-content"
                    ),
                    class_=f"metric-card {status_class}"
                )
            )
            
        return ui.div(*cards, class_="metrics-grid")


def _create_elbow_plot(runner):
    """Recreates the runner's internal plot securely for Shiny."""
    n_models = len(runner.models)
    fig, axes = plt.subplots(n_models, 2, figsize=(14, 4 * n_models), squeeze=False)
    
    speedups = runner.speedups()
    
    for idx, model_name in enumerate(runner.models):
        ax_time = axes[idx, 0]
        ax_speedup = axes[idx, 1]
        
        n_obs = runner.n_obs_grid
        t_seq = [runner.results[model_name][n]['sequential'] for n in n_obs]
        t_par = [runner.results[model_name][n]['parallel'] for n in n_obs]
        
        # 1. Fit Time Plot
        ax_time.plot(n_obs, t_seq, 'o-', color='tab:red', label='Secuencial (n_jobs=1)')
        ax_time.plot(n_obs, t_par, 's-', color='tab:green', label='Paralelo (n_jobs=-1)')
        ax_time.set_title(f'{model_name} - Tiempo de Ajuste')
        ax_time.set_xlabel('Tamaño de Serie (n_obs)')
        ax_time.set_ylabel('Tiempo (segundos)')
        ax_time.set_xscale('log')
        ax_time.grid(True, alpha=0.3)
        ax_time.legend()
        
        # 2. Speedup Plot
        s_vals = [speedups[model_name][n] for n in n_obs]
        ax_speedup.plot(n_obs, s_vals, 'o-', color='tab:blue', label='Speedup')
        ax_speedup.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Punto de Equilibrio (1x)')
        ax_speedup.axhline(y=1.1, color='tab:orange', linestyle=':', label='Umbral Recomendado (1.1x)')
        
        # Highlight elbow
        elbow = runner.elbow_threshold()[model_name]
        if elbow is not None:
            ax_speedup.axvline(x=elbow, color='tab:orange', alpha=0.4, linewidth=10, zorder=0)
            ax_speedup.text(elbow, 1.2, ' Codo', color='tab:orange', fontweight='bold')
            
        ax_speedup.set_title(f'{model_name} - Aceleración (Speedup)')
        ax_speedup.set_xlabel('Tamaño de Serie (n_obs)')
        ax_speedup.set_ylabel('Speedup (Secuencial / Paralelo)')
        ax_speedup.set_xscale('log')
        ax_speedup.grid(True, alpha=0.3)
        ax_speedup.legend()
    
    fig.patch.set_facecolor('#1a1a1a')
    for ax in axes.flatten():
        ax.set_facecolor('#2d2d2d')
        ax.tick_params(colors='white')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # Fix legend colors
        legend = ax.get_legend()
        if legend:
            for text in legend.get_texts():
                text.set_color('white')
            legend.get_frame().set_facecolor('#2d2d2d')
            legend.get_frame().set_edgecolor('white')
            
    plt.tight_layout()
    return fig
