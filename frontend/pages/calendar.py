from nicegui import ui
from datetime import datetime
from frontend.api_client import get_homepage

from frontend.theme import apply_global_theme
from frontend.pages.home import add_shared_menu

# Store events
calendar_events = []
event_type = {"value": None}

# -------------------------
# SHARED MENU FOR ALL PAGES
# -------------------------
def add_shared_menu():
    drawer = ui.left_drawer(value=False).classes("drawer-bg shadow-lg")
    with drawer:
        ui.label("Menu").classes("text-xl font-bold p-4 text-[#2E4A3A]")
        ui.separator()

        ui.button("Home", on_click=lambda: ui.navigate.to('/home')).classes("drawer-btn w-full text-left")
        ui.button("Upcoming Events", on_click=lambda: ui.notify("Upcoming Events")).classes("drawer-btn w-full text-left")
        ui.button("Upcoming Homework", on_click=lambda: ui.notify("Upcoming Homework")).classes("drawer-btn w-full text-left")
        ui.button("Calendar", on_click=lambda: ui.notify("Calendar")).classes("drawer-btn w-full text-left")
        ui.button("Add Events", on_click=lambda: ui.navigate.to('/events')).classes("drawer-btn w-full text-left")
        ui.button("Time Tracker", on_click=lambda: ui.notify("Time Tracker")).classes("drawer-btn w-full text-left")

        ui.separator().classes("my-3")
        for name in ["Settings", "Profile+", "Search", "Help"]:
            ui.button(name, on_click=lambda n=name: ui.notify(n)).classes("drawer-btn w-full text-left py-2")

        ui.separator().classes("my-4")
        ui.button("Profile", on_click=lambda: ui.navigate.to("/profile")).classes("drawer-btn w-full text-left")

        ui.separator().classes("my-4")
        ui.button("Sign Out", on_click=lambda: ui.navigate.to('/login')).classes("signout-btn w-full text-left")

    # Header
    with ui.header().classes("header-bar h-24 text-white relative flex items-center shadow-lg"):
        ui.button(icon="menu", on_click=lambda: drawer.toggle()).classes("text-white mr-4")

        with ui.element("div").classes("absolute left-1/2 -translate-x-1/2 flex flex-col items-center"):
            with ui.element("div").classes("w-14 h-14 rounded-full overflow-hidden border-2 border-[#D9C6A9] shadow-md"):
                ui.image("profile_picture_example.jpg").classes("w-full h-full object-cover")
            ui.label("Hello, Username").classes("text-lg font-semibold mt-2 text-[#F4EDE1]")

# -------------------------
# CALENDAR PAGE  (/calendar)
# -------------------------
@ui.page('/calendar')
async def events_page():
    apply_global_theme()
    add_shared_menu()

    data = await get_homepage()

    tasks = data['tasks']
    events = data['events']
    notifications = data['notifications']

    ui.label("Calendar").classes("events-title")

    with ui.column().classes("items-center space-y-6"):

        # Date selection card
        with ui.card().classes("events-card w-11/12 md:w-2/3"):
            ui.label("Select a date").classes("event-label mb-1")
            selected_date = ui.date().classes("w-full")

        # Events display card
        events_card = ui.card().classes("events-card w-11/12 md:w-2/3")
        
        def update_events_display():
            events_card.clear()
            with events_card:
                if selected_date.value:
                    # Parse selected date
                    selected_date_obj = datetime.strptime(selected_date.value, "%Y-%m-%d").date()
                    
                    # Filter events using list comprehension
                    filtered_events = [
                        event for event in events 
                        if datetime.fromisoformat(event['start_time']).date() == selected_date_obj
                    ]
                    
                    ui.label(f"Events for {selected_date.value}").classes("event-label mb-4")
                    
                    if filtered_events:
                        for event in filtered_events:
                            with ui.row().classes("items-center mb-3 p-2 border-b border-gray-200"):
                                ui.label(f"{event['name']}").classes("font-semibold mr-4")
                                ui.label(f"Type: {event['type']}").classes("text-gray-600 mr-4")
                                start_time = datetime.fromisoformat(event['start_time'])
                                end_time = datetime.fromisoformat(event['end_time'])
                                ui.label(f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}").classes("text-gray-500")
                    else:
                        ui.label("No events for this date").classes("text-gray-500 italic")
                else:
                    ui.label("Please select a date to view events").classes("text-gray-500 italic")
        
        # Update events when date changes
        selected_date.on('update:modelValue', lambda: update_events_display())
        
        # Initial display
        update_events_display()
