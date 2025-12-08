from nicegui import ui
from frontend.theme import apply_global_theme
from frontend.menutheme import add_shared_menu 


@ui.page('/timetracker')
def timetracker_page():
    apply_global_theme()
    add_shared_menu()
