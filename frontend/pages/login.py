from nicegui import ui

@ui.page('/login')
def login_page():

    # Centered layout
    with ui.row().classes('w-full h-screen justify-center items-center flex flex-col'):

        # Title
        ui.label("Remote Life Organizer").classes("earth-title")

        # Login card
        with ui.card().classes("earth-card w-96 p-6"):

            ui.label("Welcome back").classes(
                "earth-text text-xl font-bold mb-4"
            )

            username = ui.input("Username").classes("event-input w-full")
            password = ui.input(
                "Password",
                password=True,
                password_toggle_button=True
            ).classes("event-input w-full")

            message = ui.label("").classes("text-red-500 mt-2 earth-text")

            def attempt_login():
                ui.navigate.to('/home')

            ui.button("Login", on_click=attempt_login).classes(
                "event-btn w-full mt-4 py-2 text-white font-semibold rounded-lg"
            )

            ui.label("Need an account? (Coming soon)").classes(
                "earth-text text-sm mt-3 text-center"
            )

