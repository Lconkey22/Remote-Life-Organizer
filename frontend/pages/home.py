from nicegui import ui

# -------------------------
# LOGIN PAGE (NO MENU HERE)
# -------------------------
@ui.page('/login')
def login_page():
    ui.label("Login Screen").classes("text-2xl font-bold")
    ui.button("Go to Home", on_click=lambda: ui.navigate.to('/home'))


# -------------------------
# SHARED MENU FOR ALL INTERNAL PAGES
# -------------------------
def add_shared_menu():

    drawer = ui.left_drawer(value=False).classes("bg-white")
    with drawer:
        ui.label("Menu").classes("text-xl font-bold p-4")
        ui.separator()

        ui.button("Home", on_click=lambda: ui.navigate.to('/home'))
        ui.button("Upcoming Events", on_click=lambda: ui.notify("Upcoming Events"))
        ui.button("Upcoming Homework", on_click=lambda: ui.notify("Upcoming Homework"))
        ui.button("Calendar", on_click=lambda: ui.notify("Calendar"))
        ui.button("Add Events", on_click=lambda: ui.navigate.to('/events'))
        ui.button("Time Tracker", on_click=lambda: ui.notify("Time Tracker"))

        ui.separator().classes("my-3")
        for name in ["Settings", "Profile+", "Search", "Help"]:
            ui.button(name, on_click=lambda n=name: ui.notify(n)).classes(
                "w-full text-left py-2"
            )

        ui.separator().classes("my-4")
        ui.button("Profile", on_click=lambda: ui.notify("Profile")).classes("w-full text-left")

        ui.separator().classes("my-4")
        ui.button("Sign Out", on_click=lambda: ui.navigate.to('/login')).classes(
            "w-full text-left text-red-600"
        )

    # ---- HEADER ----
    with ui.header().classes("h-24 bg-blue-600 text-white relative flex items-center"):
        ui.button(icon="menu", on_click=lambda: drawer.toggle()).classes("text-white")

        with ui.element("div").classes(
            "absolute left-1/2 -translate-x-1/2 flex flex-col items-center"
        ):
            with ui.element("div").classes("w-12 h-12 rounded-full overflow-hidden"):
                ui.image("profile_picture_example.jpg").classes(
                    "w-full h-full object-cover object-center"
                )
            ui.label("Hello, Username").classes("text-lg font-semibold mt-2")


# -------------------------
# HOME PAGE
# -------------------------
@ui.page('/home')
def home_page():
    add_shared_menu()

    with ui.column().classes("p-4 items-center space-y-6"):
        for i in range(1, 4):
            with ui.card().classes("w-96 h-64 overflow-auto border-2 border-gray-300"):
                ui.label(f"Data Block {i}").classes("text-xl font-bold mb-2")
                for j in range(20):
                    ui.label(f"Item {j + 1} in block {i}")


# -------------------------
# ADD EVENTS PAGE
# -------------------------
@ui.page('/events')
def add_events_page():
    add_shared_menu()

    ui.label("Add Events Page").classes("text-2xl font-bold")
    ui.button("Back to Home", on_click=lambda: ui.navigate.to('/home'))


# -------------------------
# RUN APP
# -------------------------
ui.run()


