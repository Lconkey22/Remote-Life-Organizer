from nicegui import ui
from frontend.theme import apply_global_theme
from frontend.pages.home import add_shared_menu 


@ui.page('/upcomingevents')
def upcomingevents_page():
    apply_global_theme()
    add_shared_menu()
