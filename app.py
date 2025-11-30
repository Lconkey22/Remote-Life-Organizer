from nicegui import ui

from frontend.theme import apply_global_theme

# apply global styling ONE TIME
apply_global_theme()


# Import your page modules so their @ui.page decorators run
import frontend.pages.events
import frontend.pages.home
import frontend.pages.login

# Redirect root to login
@ui.page('/')
def index():
    ui.navigate.to('/login')

ui.run(title='Remote Life Organizer')



