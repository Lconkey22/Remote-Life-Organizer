from nicegui import ui

def create_login_page():
    @ui.page('/login')
    def login():

        # Inject custom CSS for colors + styling
        ui.add_head_html("""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Poiret+One&display=swap" rel="stylesheet">

        <style>
            body {
                background: #1B301B; /* dark green background */
                font-family: "Poiret One", sans-serif; /* GLOBAL FONT */
            }

            .title {
                color: #D9C6A9; /* light beige */
                font-size: 32px;
                font-weight: 400;
                text-align: center;
                margin-bottom: 20px;
            }

            .login-card {
                background: #ffffff;
                border-radius: 16px;
                padding: 30px;
                border: 2px solid #e5e0d3;
                box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
            }

            .login-button {
                background-color: #3a5f49 !important; /* button color */
                color: white !important;
            }

            .login-button:hover {
                background-color: #2d4b3a !important;
            }

            .input-label {
                color: #2c4a3f;
                font-weight: 400;
            }
        </style>
        """)

        # Center content on screen
        with ui.row().classes('w-full h-screen justify-center items-center flex flex-col'):

            # Title
            ui.label("Remote Life Organizer").classes("title")

            # Login card
            with ui.card().classes('login-card w-96'):

                ui.label("Welcome back 👋").classes(
                    "text-xl font-semibold text-[#2c4a3f] mb-4"
                )

                username = ui.input("Username").classes('w-full input-label')
                password = ui.input(
                    "Password",
                    password=True,
                    password_toggle_button=True
                ).classes('w-full input-label')

                message = ui.label("").classes('text-red-600 mt-2')

                # Temporary users (no database yet)
                users = {
                    "chelsie": "1234",
                    "lindsey": "abcd",
                    "nathan": "pass",
                }

                def attempt_login():
                    u = username.value
                    p = password.value

                    if u in users and users[u] == p:
                        message.set_text("")
                        ui.navigate.to('/home')
                    else:
                        message.set_text("❌ Invalid username or password")

                ui.button("Login", on_click=attempt_login).classes(
                    "w-full login-button mt-4 py-2 rounded-lg text-white font-semibold"
                )

                ui.label("Need an account? (Coming soon)").classes(
                    "text-gray-600 text-sm mt-3 text-center"
                )

