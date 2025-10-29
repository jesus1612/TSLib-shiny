# Main Shiny application for TSLib Time Series Analysis
from shiny import App, ui, reactive, render
from components.stepper import StepperComponent
from components.layout import create_app_layout
from features.upload.ui import render_upload_ui
from features.visualization.ui import render_visualization_ui
from features.model_selection.ui import render_model_selection_ui
from features.execution.ui import render_execution_ui
from features.results.ui import render_results_ui
from features.reports.ui import render_reports_ui

# Define the steps for the wizard
STEPS = [
    {
        "title": "📁 Carga de Datos",
        "description": "Sube y configura tu serie temporal"
    },
    {
        "title": "📊 Visualización",
        "description": "Explora y analiza los datos"
    },
    {
        "title": "⚙️ Selección de Modelo",
        "description": "Configura parámetros ARIMA"
    },
    {
        "title": "🚀 Ejecución",
        "description": "Ejecuta el análisis en el servidor"
    },
    {
        "title": "📈 Resultados",
        "description": "Revisa métricas y predicciones"
    },
    {
        "title": "📄 Reportes",
        "description": "Genera y descarga reportes"
    }
]

# Initialize stepper component
stepper = StepperComponent(STEPS)

# Define the UI
app_ui = ui.page_fluid(
    # Include custom CSS inline
    ui.tags.head(
        ui.tags.style(
            """
            /* TSLib Shiny App - Dark Professional Theme */
            :root {
              --bg-primary: #1a1a1a;
              --bg-secondary: #2d2d2d;
              --bg-tertiary: #3a3a3a;
              --bg-card: #252525;
              --bg-hover: #404040;
              --text-primary: #ffffff;
              --text-secondary: #b3b3b3;
              --text-muted: #cccccc;
              --accent-primary: #00d4aa;
              --accent-secondary: #0099cc;
              --accent-danger: #ff6b6b;
              --accent-warning: #ffd93d;
              --accent-success: #6bcf7f;
              --border-color: #404040;
              --border-light: #555555;
              --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.3);
              --shadow-md: 0 4px 8px rgba(0, 0, 0, 0.4);
              --shadow-lg: 0 8px 16px rgba(0, 0, 0, 0.5);
              --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
              --font-size-xs: 0.75rem;
              --font-size-sm: 0.875rem;
              --font-size-base: 1rem;
              --font-size-lg: 1.125rem;
              --font-size-xl: 1.25rem;
              --font-size-2xl: 1.5rem;
              --font-size-3xl: 1.875rem;
              --spacing-xs: 0.25rem;
              --spacing-sm: 0.5rem;
              --spacing-md: 1rem;
              --spacing-lg: 1.5rem;
              --spacing-xl: 2rem;
              --spacing-2xl: 3rem;
              --radius-sm: 0.25rem;
              --radius-md: 0.5rem;
              --radius-lg: 0.75rem;
              --radius-xl: 1rem;
            }
            
            body {
              font-family: var(--font-family);
              background-color: var(--bg-primary);
              color: var(--text-primary);
              line-height: 1.6;
              margin: 0;
              padding: 0;
              min-height: auto;
            }
            
            .main-container {
              background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
              padding: var(--spacing-sm) 0;
            }
            
            .app-header {
              background-color: var(--bg-secondary);
              border-bottom: 1px solid var(--border-color);
              padding: var(--spacing-lg) var(--spacing-xl);
              box-shadow: var(--shadow-sm);
            }
            
            .app-title {
              font-size: var(--font-size-2xl);
              font-weight: 700;
              color: var(--accent-primary);
              margin: 0;
            }
            
            .app-subtitle {
              font-size: var(--font-size-sm);
              color: var(--text-secondary);
              margin: var(--spacing-xs) 0 0 0;
            }
            
            .stepper-container {
              background-color: var(--bg-card);
              border-radius: var(--radius-lg);
              padding: var(--spacing-lg);
              margin: var(--spacing-md);
              box-shadow: var(--shadow-md);
            }
            
            .stepper-header {
              display: flex;
              justify-content: space-between;
              align-items: center;
              margin-bottom: var(--spacing-xl);
              padding-bottom: var(--spacing-lg);
              border-bottom: 1px solid var(--border-color);
            }
            
            .stepper-title {
              font-size: var(--font-size-xl);
              font-weight: 600;
              color: var(--text-primary);
              margin: 0;
            }
            
            .stepper-progress {
              font-size: var(--font-size-sm);
              color: var(--text-secondary);
              background-color: var(--bg-tertiary);
              padding: var(--spacing-sm) var(--spacing-md);
              border-radius: var(--radius-md);
            }
            
            .stepper-content {
              min-height: 200px;
              padding: var(--spacing-md) 0;
            }
            
            .stepper-navigation {
              display: flex;
              justify-content: space-between;
              align-items: center;
              margin-top: var(--spacing-xl);
              padding-top: var(--spacing-lg);
              border-top: 1px solid var(--border-color);
            }
            
            .btn {
              display: inline-flex;
              align-items: center;
              justify-content: center;
              padding: var(--spacing-sm) var(--spacing-lg);
              border: none;
              border-radius: var(--radius-md);
              font-size: var(--font-size-sm);
              font-weight: 500;
              text-decoration: none;
              cursor: pointer;
              transition: all 0.2s ease;
              min-width: 100px;
            }
            
            .btn-primary {
              background-color: var(--accent-primary);
              color: var(--bg-primary);
            }
            
            .btn-primary:hover {
              background-color: #00b894;
              transform: translateY(-1px);
              box-shadow: var(--shadow-md);
            }
            
            .btn-secondary {
              background-color: var(--bg-tertiary);
              color: var(--text-primary);
              border: 1px solid var(--border-color);
            }
            
            .btn-secondary:hover {
              background-color: var(--bg-hover);
              border-color: var(--border-light);
            }
            
            .card {
              background-color: var(--bg-card);
              border: 1px solid var(--border-color);
              border-radius: var(--radius-lg);
              padding: var(--spacing-lg);
              margin-bottom: var(--spacing-lg);
              box-shadow: var(--shadow-sm);
              transition: all 0.2s ease;
            }
            
            .card:hover {
              box-shadow: var(--shadow-md);
              border-color: var(--border-light);
            }
            
            .card-header {
              display: flex;
              justify-content: space-between;
              align-items: center;
              margin-bottom: var(--spacing-md);
              padding-bottom: var(--spacing-sm);
              border-bottom: 1px solid var(--border-color);
            }
            
            .card-title {
              font-size: var(--font-size-lg);
              font-weight: 600;
              color: var(--text-primary);
              margin: 0;
            }
            
            .card-subtitle {
              font-size: var(--font-size-sm);
              color: var(--text-secondary);
              margin: var(--spacing-xs) 0 0 0;
            }
            
            .file-upload-area {
              border: 2px dashed var(--border-color);
              border-radius: var(--radius-lg);
              padding: var(--spacing-2xl);
              text-align: center;
              background-color: var(--bg-tertiary);
              transition: all 0.2s ease;
              cursor: pointer;
            }
            
            .file-upload-area:hover {
              border-color: var(--accent-primary);
              background-color: var(--bg-hover);
            }
            
            .file-upload-icon {
              font-size: var(--font-size-3xl);
              color: var(--accent-primary);
              margin-bottom: var(--spacing-md);
            }
            
            .file-upload-text {
              font-size: var(--font-size-lg);
              color: var(--text-primary);
              margin-bottom: var(--spacing-sm);
            }
            
            .file-upload-hint {
              font-size: var(--font-size-sm);
              color: var(--text-secondary);
            }
            
            .metrics-grid {
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
              gap: var(--spacing-lg);
              margin-bottom: var(--spacing-xl);
            }
            
            .metric-card {
              background-color: var(--bg-card);
              border: 1px solid var(--border-color);
              border-radius: var(--radius-lg);
              padding: var(--spacing-lg);
              text-align: center;
              box-shadow: var(--shadow-sm);
            }
            
            .metric-value {
              font-size: var(--font-size-2xl);
              font-weight: 700;
              color: var(--accent-primary);
              margin-bottom: var(--spacing-xs);
            }
            
            .metric-label {
              font-size: var(--font-size-sm);
              color: var(--text-secondary);
              margin: 0;
            }
            
            .d-none { display: none; }
            .d-block { display: block; }
            .d-flex { display: flex; }
            .d-grid { display: grid; }
            
            .text-center { text-align: center; }
            .text-left { text-align: left; }
            .text-right { text-align: right; }
            
            .text-muted { color: var(--text-muted); }
            
            .mt-1 { margin-top: var(--spacing-xs); }
            .mt-2 { margin-top: var(--spacing-sm); }
            .mt-3 { margin-top: var(--spacing-md); }
            .mt-4 { margin-top: var(--spacing-lg); }
            .mt-5 { margin-top: var(--spacing-xl); }
            
            .mb-1 { margin-bottom: var(--spacing-xs); }
            .mb-2 { margin-bottom: var(--spacing-sm); }
            .mb-3 { margin-bottom: var(--spacing-md); }
            .mb-4 { margin-bottom: var(--spacing-lg); }
            .mb-5 { margin-bottom: var(--spacing-xl); }
            
            .gap-2 { gap: var(--spacing-sm); }
            .gap-3 { gap: var(--spacing-md); }
            
            .justify-center { justify-content: center; }
            .justify-between { justify-content: space-between; }
            .align-center { align-items: center; }
            
            /* Form elements styling */
            .form-label {
              color: var(--text-primary) !important;
              font-weight: 500;
              margin-bottom: var(--spacing-xs);
              display: block;
            }
            
            .form-help {
              color: var(--text-secondary) !important;
              font-size: var(--font-size-xs);
              margin-top: var(--spacing-xs);
            }
            
            /* Ensure all labels are visible */
            label {
              color: var(--text-primary) !important;
            }
            
            /* Ensure all small text is visible */
            small {
              color: var(--text-secondary) !important;
            }
            
            /* Ensure all text elements are visible */
            h1, h2, h3, h4, h5, h6 {
              color: var(--text-primary) !important;
            }
            
            p, div, span {
              color: var(--text-primary) !important;
            }
            
            /* Specific styling for execution step */
            .execution-status, .estimated-time, .progress-step {
              color: var(--text-secondary) !important;
            }
            
            /* Data preview styling */
            #data_preview_placeholder {
              color: var(--text-secondary) !important;
            }
            
            /* Input styling */
            input[type="number"], input[type="text"], input[type="email"], input[type="password"], 
            select, textarea {
              background-color: var(--bg-tertiary);
              border: 1px solid var(--border-color);
              border-radius: var(--radius-md);
              color: var(--text-primary);
              padding: var(--spacing-sm) var(--spacing-md);
              font-size: var(--font-size-sm);
            }
            
            input[type="number"]:focus, input[type="text"]:focus, input[type="email"]:focus, 
            input[type="password"]:focus, select:focus, textarea:focus {
              outline: none;
              border-color: var(--accent-primary);
              box-shadow: 0 0 0 2px rgba(0, 212, 170, 0.2);
            }
            
            /* Switch styling */
            .form-check-input {
              background-color: var(--bg-tertiary);
              border-color: var(--border-color);
            }
            
            .form-check-input:checked {
              background-color: var(--accent-primary);
              border-color: var(--accent-primary);
            }
            
            .form-check-label {
              color: var(--text-primary);
              margin-left: var(--spacing-sm);
            }
            
            /* Slider styling */
            input[type="range"] {
              background: var(--bg-tertiary);
              border-radius: var(--radius-md);
            }
            
            input[type="range"]::-webkit-slider-thumb {
              background: var(--accent-primary);
              border-radius: 50%;
            }
            
            input[type="range"]::-moz-range-thumb {
              background: var(--accent-primary);
              border-radius: 50%;
            }
            
            /* Status indicators */
            .status-indicator {
              padding: var(--spacing-xs) var(--spacing-sm);
              border-radius: var(--radius-sm);
              font-size: var(--font-size-sm);
              font-weight: 500;
            }
            
            .status-info {
              background-color: rgba(0, 153, 204, 0.2);
              color: var(--accent-secondary);
              border: 1px solid var(--accent-secondary);
            }
            
            .status-success {
              background-color: rgba(107, 207, 127, 0.2);
              color: var(--accent-success);
              border: 1px solid var(--accent-success);
            }
            
            .status-warning {
              background-color: rgba(255, 217, 61, 0.2);
              color: var(--accent-warning);
              border: 1px solid var(--accent-warning);
            }
            
            .status-danger {
              background-color: rgba(255, 107, 107, 0.2);
              color: var(--accent-danger);
              border: 1px solid var(--accent-danger);
            }
            
            /* Progress steps */
            .progress-step {
              color: var(--text-secondary);
              font-size: var(--font-size-sm);
              padding: var(--spacing-xs) 0;
              border-left: 2px solid var(--border-color);
              padding-left: var(--spacing-sm);
              margin-bottom: var(--spacing-xs);
            }
            
            .progress-list {
              margin-top: var(--spacing-sm);
            }
            
            /* Button variants */
            .btn-lg {
              padding: var(--spacing-md) var(--spacing-xl);
              font-size: var(--font-size-lg);
            }
            
            .btn-warning {
              background-color: var(--accent-warning);
              color: var(--bg-primary);
            }
            
            .btn-warning:hover {
              background-color: #e6c200;
              transform: translateY(-1px);
              box-shadow: var(--shadow-md);
            }
            
            .btn-danger {
              background-color: var(--accent-danger);
              color: var(--bg-primary);
            }
            
            .btn-danger:hover {
              background-color: #ff5252;
              transform: translateY(-1px);
              box-shadow: var(--shadow-md);
            }
            
            /* File upload styling */
            .file-input-hidden {
              display: none !important;
            }
            
            .file-upload-wrapper {
              position: relative;
            }
            
            .file-upload-area {
              border: 2px dashed var(--border-color);
              border-radius: var(--radius-lg);
              padding: var(--spacing-2xl);
              text-align: center;
              background-color: var(--bg-tertiary);
              transition: all 0.2s ease;
              cursor: pointer;
              position: relative;
            }
            
            .file-upload-area:hover {
              border-color: var(--accent-primary);
              background-color: var(--bg-hover);
            }
            
            .file-upload-area:active {
              transform: scale(0.98);
            }
            </style>
            <script>
            // Handle custom messages from server
            Shiny.addCustomMessageHandler("update_preview", function(message) {
              // Hide placeholder and show content
              const placeholder = document.getElementById("data_preview_placeholder");
              const content = document.getElementById("data_preview_content");
              
              if (placeholder && content) {
                placeholder.style.display = "none";
                content.classList.remove("d-none");
                content.classList.add("d-block");
                
                // Update file info
                const rowCount = document.getElementById("row_count");
                const colCount = document.getElementById("col_count");
                const fileSize = document.getElementById("file_size");
                
                if (rowCount) rowCount.textContent = "Filas: " + message.rows;
                if (colCount) colCount.textContent = "Columnas: " + message.columns;
                if (fileSize) fileSize.textContent = "Tamaño: " + message.size;
              }
            });
            </script>
            """
        )
    ),
    
    # Main app layout
    create_app_layout(
        title="TSLib - Análisis de Series de Tiempo",
        subtitle="Pipeline completo para análisis avanzado con modelos ARIMA"
    ),
    
    
    # Stepper header output
    ui.output_ui("stepper_header"),
    
    # Main content area
    ui.div(
        # Step content will be rendered here
        ui.output_ui("step_content"),
        class_="container-fluid"
    ),
    
    # Stepper navigation output
    ui.output_ui("stepper_navigation")
)

# Define the server logic
def server(input, output, session):
    """Server logic with reactive event handling"""
    
    # Reactive values for app state
    app_state = reactive.Value({
        "current_step": 0,
        "data_loaded": False,
        "analysis_complete": False,
        "uploaded_data": None,
        "selected_model": None,
        "results": None
    })
    
    # Stepper header renderer
    @render.ui
    def stepper_header():
        """Render stepper header reactively"""
        current_step = app_state.get()["current_step"]
        return ui.div(
            ui.div(
                ui.tags.h2(
                    STEPS[current_step]["title"],
                    class_="stepper-title"
                ),
                ui.div(
                    f"Paso {current_step + 1} de {len(STEPS)}",
                    class_="stepper-progress"
                ),
                class_="stepper-header"
            ),
            class_="stepper-container"
        )
    
    # Stepper navigation renderer
    @render.ui
    def stepper_navigation():
        """Render stepper navigation reactively"""
        current_step = app_state.get()["current_step"]
        return ui.div(
            ui.div(
                ui.input_action_button(
                    "prev_step",
                    "← Anterior",
                    class_="btn btn-secondary"
                ) if current_step > 0 else ui.div(),
                class_="d-flex"
            ),
            ui.div(
                ui.input_action_button(
                    "next_step",
                    "Siguiente →" if current_step < len(STEPS) - 1 else "Finalizar",
                    class_="btn btn-primary"
                ),
                class_="d-flex"
            ),
            class_="stepper-navigation"
        )
    
    # Step content renderer
    @render.ui
    def step_content():
        """Render content for current step"""
        current_step = app_state.get()["current_step"]
        
        if current_step == 0:
            return render_upload_ui()
        elif current_step == 1:
            return render_visualization_ui()
        elif current_step == 2:
            return render_model_selection_ui()
        elif current_step == 3:
            return render_execution_ui()
        elif current_step == 4:
            return render_results_ui()
        elif current_step == 5:
            return render_reports_ui()
        else:
            return ui.div("Paso no válido", class_="alert alert-danger")
    
    # Navigation event handlers
    @reactive.effect
    @reactive.event(input.next_step)
    def handle_next_step():
        """Handle next step button click"""
        current_state = app_state.get()
        current_step = current_state["current_step"]
        
        # Validate current step before proceeding
        if validate_current_step(current_step, current_state):
            if current_step < len(STEPS) - 1:
                new_state = current_state.copy()
                new_state["current_step"] = current_step + 1
                app_state.set(new_state)
                stepper.current_step = current_step + 1
    
    @reactive.effect
    @reactive.event(input.prev_step)
    def handle_prev_step():
        """Handle previous step button click"""
        current_state = app_state.get()
        current_step = current_state["current_step"]
        
        if current_step > 0:
            new_state = current_state.copy()
            new_state["current_step"] = current_step - 1
            app_state.set(new_state)
            stepper.current_step = current_step - 1
    
    # File upload handler
    @reactive.effect
    @reactive.event(input.file_upload)
    def handle_file_upload():
        """Handle file upload"""
        if input.file_upload() is not None:
            # Simulate data loading
            new_state = app_state.get()
            new_state["data_loaded"] = True
            new_state["uploaded_data"] = {
                "filename": input.file_upload()[0]["name"],
                "size": input.file_upload()[0]["size"],
                "rows": 1000,  # Mock data
                "columns": 2
            }
            app_state.set(new_state)
            
            # Update preview elements via JavaScript
            session.send_custom_message("update_preview", {
                "filename": input.file_upload()[0]["name"],
                "size": f"{input.file_upload()[0]['size'] / 1024:.1f} KB",
                "rows": "1000",
                "columns": "2"
            })
    
    # Model execution handler
    @reactive.effect
    @reactive.event(input.start_execution)
    def handle_start_execution():
        """Handle model execution start"""
        # Simulate analysis execution
        new_state = app_state.get()
        new_state["analysis_complete"] = True
        new_state["selected_model"] = "ARIMA(1,1,1)"
        new_state["results"] = {
            "aic": 1234.56,
            "bic": 1256.78,
            "rmse": 15.23,
            "mae": 12.45
        }
        app_state.set(new_state)
    
    # Report generation handler
    @reactive.effect
    @reactive.event(input.generate_report)
    def handle_generate_report():
        """Handle report generation"""
        # Simulate report generation
        ui.notification_show(
            "Reporte generado exitosamente",
            type="success",
            duration=3
        )
    
    def validate_current_step(step: int, state: dict) -> bool:
        """Validate if current step can proceed to next"""
        if step == 0:  # Upload step
            return state["data_loaded"]
        elif step == 1:  # Visualization step
            return state["data_loaded"]
        elif step == 2:  # Model selection step
            return state["data_loaded"]
        elif step == 3:  # Execution step
            return state["data_loaded"]
        elif step == 4:  # Results step
            return state["analysis_complete"]
        elif step == 5:  # Reports step
            return state["analysis_complete"]
        return True
    
    # Reactive UI updates based on state
    @reactive.effect
    def update_ui_state():
        """Update UI elements based on app state"""
        state = app_state.get()
        
        # Update step indicators
        if state["data_loaded"]:
            # Show data preview elements
            pass
        
        if state["analysis_complete"]:
            # Show results elements
            pass

# Create the Shiny app
app = App(app_ui, server)

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
