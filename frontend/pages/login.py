from nicegui import ui

def create_login_page():
    @ui.page('/login')
    def login():

        # Inject custom CSS for colors + styling
        ui.add_head_html("""
        <style>
            body {
                background: #f7f3eb; /* light beige */
                font-family: 'Inter', sans-serif;
            }
            .login-card {
                background: #ffffff;
                border-radius: 16px;
                padding: 30px;
                border: 2px solid #e5e0d3;
                box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
            }
            .title {
                color: #2c4a3f; /* dark forest green */
                font-size: 28px;
                font-weight: 700;
                text-align: center;
                margin-bottom: 20px;
            }
            .login-button {
                background-color: #3a5f49 !important; /* forest green */
                color: white !important;
            }
            .login-button:hover {
                background-color: #2d4b3a !important;
            }
            .input-label {
                color: #2c4a3f;
                font-weight: 600;
            }
        </style>
        """)

        # Center content on screen
        with ui.column().classes('items-center justify-center min-h-screen'):

            # Title
            ui.label("Remote Life Organizer").classes("title")

            # Login card
            with ui.card().classes('login-card w-96'):

                ui.label("Welcome back 👋").classes("text-xl font-semibold text-[#2c4a3f] mb-4")

                username = ui.input("Username").classes('w-full input-label')
                password = ui.input("Password", password=True, password_toggle_button=True).classes('w-full input-label')

                message = ui.label("").classes('text-red-600 mt-2')

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

