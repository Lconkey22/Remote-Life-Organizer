from nicegui import ui
from frontend.theme import apply_global_theme

import frontend.pages.events
import frontend.pages.home
import frontend.pages.login
import frontend.pages.profile
import frontend.pages.upcominghomework
import frontend.pages.upcomingevents
import frontend.pages.timetracker
import frontend.pages.calendar

import backend.main

# Redirect root to login
@ui.page('/')
def index():
    ui.navigate.to('/login')

ui.run(title='Remote Life Organizer')




