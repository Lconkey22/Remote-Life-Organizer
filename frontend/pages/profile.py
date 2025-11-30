from nicegui import ui
from frontend.theme import apply_global_theme
from frontend.pages.home import add_shared_menu   # reuse same shared menu

# -------------------------
# PROFILE PAGE  (/profile)
# -------------------------
@ui.page('/profile')
def profile_page():
    apply_global_theme()
    add_shared_menu()

    # ----- PROFILE TITLE -----
    ui.label("User Profile").classes("home-title text-center mt-6")

    # ----- PROFILE INFO CARD -----
    with ui.column().classes("p-6 items-center space-y-6"):
        with ui.card().classes("home-card w-96 p-6 space-y-3"):

            ui.label("Username: Username").classes("item-text")
            ui.label("Email: user@example.com").classes("item-text")
            ui.label("Member Since: 2025").classes("item-text")

            ui.button(
                "Edit Profile",
                on_click=lambda: ui.notify("Edit Profile Coming Soon!")
            ).classes("event-btn w-full py-2 text-white rounded-lg")

            
