from nicegui import ui

# Import your page modules so their @ui.page decorators run
import frontend.pages.login
import frontend.pages.home
import frontend.pages.events

# Redirect root to login
@ui.page('/')
def index():
    ui.navigate.to('/login')

ui.run(title='Remote Life Organizer')



