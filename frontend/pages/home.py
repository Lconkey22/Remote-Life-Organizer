from nicegui import ui
from frontend.theme import apply_global_theme

# -------------------------
# SHARED MENU FOR ALL PAGES
# -------------------------
def add_shared_menu():
    # Apply theme styles
    apply_global_theme()

    # ---- Drawer ----
    drawer = ui.left_drawer(value=False).classes("drawer-bg shadow-lg")
    with drawer:
        ui.label("Menu").classes("text-xl font-bold p-4 text-[#2E4A3A]")
        ui.separator()

        ui.button("Home", on_click=lambda: ui.navigate.to('/home')).classes("drawer-btn w-full text-left")
        ui.button("Upcoming Events", on_click=lambda: ui.navigate.to("/upcomingevents")).classes("drawer-btn w-full text-left")
        ui.button("Upcoming Homework", on_click=lambda: ui.navigate.to('/homework')).classes("drawer-btn w-full text-left")
        ui.button("Calendar", on_click=lambda: ui.notify("Calendar")).classes("drawer-btn w-full text-left")
        ui.button("Add Events", on_click=lambda: ui.navigate.to('/events')).classes("drawer-btn w-full text-left")
        ui.button("Time Tracker", on_click=lambda: ui.navigate.to("/timetracker")).classes("drawer-btn w-full text-left")

        ui.separator().classes("my-3")
        for name in ["Settings", "Profile+", "Search", "Help"]:
            ui.button(name, on_click=lambda n=name: ui.notify(n)).classes("drawer-btn w-full text-left py-2")

        ui.separator().classes("my-4")
        ui.button("Profile", on_click=lambda: ui.navigate.to('/profile')).classes("drawer-btn w-full text-left")

        ui.separator().classes("my-4")
        ui.button("Sign Out", on_click=lambda: ui.navigate.to('/login')).classes(
            "signout-btn w-full text-left py-2"
        )

    # ---- Header ----
    with ui.header().classes("header-bar h-24 text-white relative flex items-center shadow-lg"):
        ui.button(icon="menu", on_click=lambda: drawer.toggle()).classes("text-white mr-4")

        with ui.element("div").classes("absolute left-1/2 -translate-x-1/2 flex flex-col items-center"):
            with ui.element("div").classes("w-14 h-14 rounded-full overflow-hidden border-2 border-[#D9C6A9] shadow-md"):
                ui.image("profile_picture_example.jpg").classes("w-full h-full object-cover")
            ui.label("Hello, Username").classes("text-lg font-semibold mt-2 text-[#F4EDE1]")


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
