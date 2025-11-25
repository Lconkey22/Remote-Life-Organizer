# -------------------------
# USER PROFILE PAGE
# -------------------------

from nicegui import ui

def create_profile_page():
    @ui.page('/profile')
    def profile():
        
            # ----- DRAWER MENU -----
        drawer = ui.left_drawer(value=False).classes("bg-white")
        with drawer:
            ui.label("Menu").classes("text-xl font-bold p-4")
            ui.separator()
            ui.button("Home", on_click=lambda: ui.navigate.to("/"))
            ui.button("Upcoming Events", on_click=lambda: ui.navigate.to("/upcoming-events"))
            ui.button("Upcoming Homework", on_click=lambda: ui.notify("Upcoming Homework"))
            ui.button("Calendar", on_click=lambda: ui.notify("Calendar"))
            ui.button("Add Events", on_click=lambda: ui.navigate.to("/add-events"))
            ui.button("Time Tracker", on_click=lambda: ui.notify("Time Tracker"))

            ui.separator().classes("my-3")
            for name in ["Settings", "Profile+", "Search", "Help"]:
                ui.button(name, on_click=lambda n=name: ui.notify(n)).classes("w-full text-left py-2")

            ui.separator().classes("my-4")
            ui.button("Profile", on_click=lambda: ui.navigate.to("/profile")).classes("w-full text-left")

            ui.separator().classes("my-4")
            ui.button("Sign Out", on_click=lambda: ui.open('/login')).classes(
                "w-full text-left text-red-600"
            )

        # ----- HEADER -----
        with ui.header().classes("h-24 bg-blue-600 text-white relative flex items-center"):
            ui.button(icon="menu", on_click=lambda: drawer.toggle()).classes("text-white")
            with ui.element("div").classes("absolute left-1/2 -translate-x-1/2 flex flex-col items-center"):
                with ui.element("div").classes("w-12 h-12 rounded-full overflow-hidden"):
                    ui.image("profile_picture_example.jpg").classes("w-full h-full object-cover")
                ui.label("Hello, Username").classes("text-lg font-semibold mt-2")

        # ----- PROFILE CONTENT -----
        with ui.column().classes("p-6 items-center space-y-6"):
            ui.label("👤 User Profile").classes("text-3xl font-bold")

            with ui.card().classes("w-96 p-6 border-2 border-gray-300 space-y-3"):
                ui.label("Username: Username").classes("text-lg")
                ui.label("Email: user@example.com").classes("text-lg")
                ui.label("Member Since: 2025").classes("text-lg")

                ui.button("Edit Profile",
                          on_click=lambda: ui.notify("Edit Profile Coming Soon!")
                         ).classes("bg-blue-600 text-white w-full py-2 rounded-lg")
            
