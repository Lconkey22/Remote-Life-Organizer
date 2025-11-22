from nicegui import ui

def create_login_page():
    @ui.page('/login')
    def login():
        ui.markdown("## Remote Life Organizer Login").classes('text-center mt-8')

        with ui.card().classes('w-80 p-6 mx-auto mt-6 shadow-xl'):
            username = ui.input("Username").classes('w-full')
            password = ui.input("Password", password=True, password_toggle_button=True).classes('w-full')

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
                'w-full bg-blue-600 text-white mt-4'
            )

