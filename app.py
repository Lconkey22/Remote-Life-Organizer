from nicegui import ui

# Redirect root ("/") → login page
@ui.page('/')
def index():
    ui.navigate.to('/login')

# No manual imports needed:
# Pages will auto-register because they use @ui.page() in their own files.

ui.run(title='Remote Life Organizer')


