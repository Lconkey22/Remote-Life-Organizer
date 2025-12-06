from nicegui import ui
from frontend.theme import apply_global_theme

import frontend.pages.events
import frontend.pages.home
import frontend.pages.login
import frontend.pages.profile 
import frontend.pages.upcominghomework

# Redirect root to login
@ui.page('/')
def index():
    ui.navigate.to('/login')

ui.run(title='Remote Life Organizer')




