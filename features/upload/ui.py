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
            ui.output_ui("upload_area_ui"),
            ui.div(
                ui.tags.h5("Vista Prevía"),
                ui.div(
                    ui.output_ui("data_preview_ui"),
                    id="data_preview_container"
                ),
                class_="mt-3"
            ),
            # Column selection section
            ui.output_ui("column_selection_ui")
        )
    )
