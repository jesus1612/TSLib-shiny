# Upload feature UI components
from shiny import ui
from components.layout import create_card, create_form_group, create_file_upload_area, create_data_table

def render_upload_ui() -> ui.Tag:
    """Render upload step UI components"""
    
    # Single focused upload section
    return create_card(
        title="📁 Carga de Datos",
        subtitle="Sube tu archivo CSV o Excel",
        content=ui.div(
            create_file_upload_area(
                input_id="file_upload",
                label="Seleccionar archivo",
                accept=".csv,.xlsx,.xls"
            ),
            ui.div(
                ui.tags.p("Formatos soportados: CSV, Excel (.xlsx, .xls)", class_="text-muted"),
                ui.tags.p("Tamaño máximo: 50MB", class_="text-muted"),
                class_="mt-2"
            ),
            ui.div(
                ui.tags.h4("Vista Previa:"),
                ui.div(
                    ui.output_ui("data_preview_ui"),
                    id="data_preview_container"
                ),
                class_="mt-3"
            )
        )
    )
