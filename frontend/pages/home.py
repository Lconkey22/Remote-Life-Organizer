from nicegui import ui
from frontend.theme import apply_global_theme
from frontend.menutheme import add_shared_menu 


# -------------------------
# HOME PAGE  (/home)
# -------------------------
@ui.page('/home')
def home_page():
    apply_global_theme()
    add_shared_menu()

    ui.label("Your Dashboard").classes("home-title text-center mt-6")

    with ui.column().classes("p-4 items-center space-y-8 w-full"):
        for i in range(1, 4):  # three cards
            with ui.card().classes("home-card w-10/12 md:w-2/3 lg:w-1/2 p-4"):
                ui.label(f"Data Block {i}").classes("text-xl font-bold mb-2 text-[#2E4A3A]")

                for j in range(5):
                    ui.label(f"• Item {j + 1} in block {i}").classes("item-text")
