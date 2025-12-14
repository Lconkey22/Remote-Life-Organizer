from nicegui import ui
from frontend.theme import apply_global_theme

def add_shared_menu():
    apply_global_theme()

    # ----- DRAWER -----
    drawer = ui.left_drawer(value=False).classes("drawer-bg shadow-lg")
    with drawer:
        ui.label("Menu").classes("text-xl font-bold p-4 text-[#2E4A3A]")
        ui.separator()

        buttons = [
            ("Home", "/home"),
            ("Upcoming Events", "/upcomingevents"),
            ("Upcoming Homework", "/upcominghomework"),
            ("Calendar", "/calendar"),
            ("Add Events", "/events"),
            ("Time Tracker", "timetracker")
        ]

        for text, link in buttons:
            if link:
                ui.button(text, on_click=lambda l=link: ui.navigate.to(l)).classes("drawer-btn")
            else:
                ui.button(text, on_click=lambda t=text: ui.notify(t)).classes("drawer-btn")

        ui.separator().classes("my-3")

        for name in ["Settings", "Profile+", "Search", "Help"]:
            ui.button(name, on_click=lambda n=name: ui.notify(n)).classes("drawer-btn")

        ui.separator().classes("my-4")
        ui.button("Profile", on_click=lambda: ui.navigate.to("/profile")).classes("drawer-btn")

        ui.separator().classes("my-4")
        ui.button("Sign Out", on_click=lambda: ui.navigate.to("/login")).classes("signout-btn")


    # ---------- HEADER ----------
    with ui.header().classes(
        "header-bar h-20 flex items-center px-4 shadow-md"
    ):
        # Hamburger icon
        ui.button(
            icon="menu",
            on_click=lambda: drawer.toggle()
        ).classes("text-[#F4EDE1]")   # beige icon

        # Center title/profile area
        with ui.element("div").classes(
            "absolute left-1/2 -translate-x-1/2 flex flex-col items-center"
        ):
            with ui.element("div").classes(
                "w-12 h-12 rounded-full overflow-hidden border-2 border-[#D9C6A9]"
            ):
                ui.image("profile_picture_example.jpg").classes("w-full h-full object-cover")

            ui.label("Hello, Username").classes(
                "text-[#F4EDE1] font-semibold mt-1"
            )

