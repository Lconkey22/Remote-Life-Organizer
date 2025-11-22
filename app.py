from nicegui import ui

from frontend.pages.home import create_home_page
from frontend.pages.login import create_login_page

# Register pages
create_login_page()
create_home_page()

# Optional redirect from root → login
@ui.page('/')
def index():
    ui.navigate.to('/login')

ui.run(title='Remote Life Organizer')

