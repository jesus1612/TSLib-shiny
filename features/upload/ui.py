# Upload feature UI components
from shiny import ui
from components.layout import create_card, create_form_group, create_file_upload_area, create_data_table

def render_upload_ui() -> ui.Tag:
    """Render upload step UI components"""
    
    # File upload section
    upload_section = create_card(
        title="📁 Carga de Datos",
        subtitle="Sube tu archivo CSV o Excel con la serie temporal",
        content=ui.div(
            create_file_upload_area(
                input_id="file_upload",
                label="Seleccionar archivo",
                accept=".csv,.xlsx,.xls"
            ),
            ui.div(
                ui.p("Formatos soportados: CSV, Excel (.xlsx, .xls)", class_="text-muted"),
                ui.p("Tamaño máximo: 50MB", class_="text-muted"),
                class_="mt-2"
            )
        )
    )
    
    # Data preview section
    preview_section = create_card(
        title="👁️ Vista Previa de Datos",
        subtitle="Revisa los datos cargados antes de continuar",
        content=ui.div(
            ui.div(
                ui.p("No hay datos cargados", class_="text-muted text-center"),
                class_="d-none",
                id="no_data_message"
            ),
            ui.div(
                ui.div(
                    ui.div("📊", class_="file-upload-icon"),
                    ui.div("Carga un archivo para ver la vista previa", class_="file-upload-text"),
                    class_="file-upload-area"
                ),
                id="data_preview_placeholder"
            ),
            ui.div(
                ui.div(
                    ui.h4("Primeras 10 filas:"),
                    ui.div(id="data_table"),
                    class_="mt-3"
                ),
                ui.div(
                    ui.h4("Información del dataset:"),
                    ui.div(
                        ui.div("Filas: 0", id="row_count"),
                        ui.div("Columnas: 0", id="col_count"),
                        ui.div("Tamaño: 0 KB", id="file_size"),
                        class_="metrics-grid"
                    ),
                    class_="mt-3"
                ),
                id="data_info",
                class_="d-none"
            )
        )
    )
    
    # Column selection section
    column_section = create_card(
        title="⚙️ Configuración de Columnas",
        subtitle="Selecciona las columnas de tiempo y valores",
        content=ui.div(
            ui.div(
                create_form_group(
                    label="Columna de Tiempo",
                    control=ui.input_select(
                        "time_column",
                        "Seleccionar columna de tiempo",
                        choices={},
                        class_="form-control"
                    ),
                    help_text="Columna que contiene las fechas o timestamps"
                ),
                create_form_group(
                    label="Columna de Valores",
                    control=ui.input_select(
                        "value_column",
                        "Seleccionar columna de valores",
                        choices={},
                        class_="form-control"
                    ),
                    help_text="Columna que contiene los valores de la serie temporal"
                ),
                class_="d-none",
                id="column_selection"
            ),
            ui.div(
                ui.p("Carga datos para configurar las columnas", class_="text-muted text-center"),
                id="column_placeholder"
            )
        )
    )
    
    # Data validation section
    validation_section = create_card(
        title="✅ Validación de Datos",
        subtitle="Verificación de calidad de los datos",
        content=ui.div(
            ui.div(
                ui.div(
                    ui.div("🔍", class_="file-upload-icon"),
                    ui.div("Los datos se validarán después de la carga", class_="file-upload-text"),
                    class_="file-upload-area"
                ),
                id="validation_placeholder"
            ),
            ui.div(
                ui.div(
                    ui.h4("Resultados de validación:"),
                    ui.div(
                        ui.div("✓ Datos válidos", class_="status-indicator status-success"),
                        ui.div("✓ Sin valores faltantes", class_="status-indicator status-success"),
                        ui.div("✓ Formato de fecha correcto", class_="status-indicator status-success"),
                        class_="mt-2"
                    ),
                    class_="mt-3"
                ),
                ui.div(
                    ui.h4("Estadísticas básicas:"),
                    ui.div(
                        ui.div("Media: 0", id="mean_value"),
                        ui.div("Desv. Estándar: 0", id="std_value"),
                        ui.div("Mínimo: 0", id="min_value"),
                        ui.div("Máximo: 0", id="max_value"),
                        class_="metrics-grid"
                    ),
                    class_="mt-3"
                ),
                id="validation_results",
                class_="d-none"
            )
        )
    )
    
    return ui.div(
        upload_section,
        preview_section,
        column_section,
        validation_section,
        class_="upload-container"
    )
