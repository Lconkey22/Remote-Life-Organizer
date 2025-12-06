def add_shared_menu():

    drawer = ui.left_drawer(value=False).classes("earth-drawer shadow-xl")
    with drawer:

        ui.label("Menu").classes("earth-menu-title")

        menu_items = [
            ("Home", "/home"),
            ("Upcoming Events", "/upcomingevents"),
            ("Upcoming Homework", "/upcominghomework"),
            ("Calendar", None),
            ("Add Events", "/events"),
            ("Time Tracker", "/timetracker"),
        ]

        for label, route in menu_items:
            ui.button(
                label,
                on_click=(lambda r=route: ui.navigate.to(r)) if route else (lambda l=label: ui.notify(l))
            ).classes("earth-menu-btn")

        ui.separator().classes("my-4")

        extra_items = ["Settings", "Profile+", "Search", "Help"]
        for name in extra_items:
            ui.button(name, on_click=lambda n=name: ui.notify(n)).classes("earth-menu-btn")

        ui.separator().classes("my-4")

        ui.button("Profile", on_click=lambda: ui.navigate.to("/profile")).classes("earth-menu-btn")

        ui.button("Sign Out", on_click=lambda: ui.navigate.to('/login')).classes(
            "earth-signout-btn"
        )

    # ---- HEADER BAR ----
    with ui.header().classes("earth-header shadow-md"):
        ui.button(icon="menu", on_click=lambda: drawer.toggle()).classes("earth-menu-icon")
