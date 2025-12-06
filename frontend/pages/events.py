from nicegui import ui
from datetime import datetime

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
        ui.button("Upcoming Events", on_click=lambda: ui.navigate.to("/upcomingevents")).classes("drawer-btn w-full text-left")
        ui.button("Upcoming Homework", on_click=lambda: ui.navigate.to("/upcominghomework")).classes("drawer-btn w-full text-left")
        ui.button("Calendar", on_click=lambda: ui.notify("Calendar")).classes("drawer-btn w-full text-left")
        ui.button("Add Events", on_click=lambda: ui.navigate.to('/events')).classes("drawer-btn w-full text-left")
        ui.button("Time Tracker", on_click=lambda: ui.navigate.to("/timetracker")).classes("drawer-btn w-full text-left")

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
# CREATE EVENT FUNCTION
# -------------------------
def create_event(selected_date, event_type_name, start_time, end_time):
    if not selected_date or not event_type_name or not start_time or not end_time:
        ui.notify("All fields required", color="red")
        return

    try:
        datetime.strptime(start_time.strip(), "%I:%M %p")
        datetime.strptime(end_time.strip(), "%I:%M %p")
    except ValueError:
        ui.notify("Use format: HH:MM AM/PM", color="red")
        return

    calendar_events.append({
        "type": event_type_name,
        "date": selected_date,
        "start time": start_time.upper(),
        "end time": end_time.upper()
    })

    ui.notify("Event Added!", color="green")


# -------------------------
# EVENTS PAGE  (/events)
# -------------------------
@ui.page('/events')
def events_page():
    apply_global_theme()
    add_shared_menu()

    ui.label("Add a New Event").classes("events-title")

    with ui.column().classes("items-center space-y-6"):

        # Event type buttons
        ui.button("Work Shift", on_click=lambda: event_type.update(value="Work")).classes("event-btn w-64")
        ui.button("Family Event", on_click=lambda: event_type.update(value="Family")).classes("event-btn w-64")
        ui.button("School Event", on_click=lambda: event_type.update(value="School")).classes("event-btn w-64")
        ui.button("Other Event", on_click=lambda: event_type.update(value="Other")).classes("event-btn w-64")

        # Event input card
        with ui.card().classes("events-card w-11/12 md:w-2/3"):

            ui.label("Select a date").classes("event-label mb-1")
            selected_date = ui.date().classes("w-full")

            ui.separator().classes("my-4")

            ui.label("Start time (HH:MM AM/PM)").classes("event-label")
            start_input = ui.input().classes("event-input w-64")

            ui.label("End time (HH:MM AM/PM)").classes("event-label mt-3")
            end_input = ui.input().classes("event-input w-64")

            ui.button(
                "Save Event",
                on_click=lambda: create_event(
                    selected_date.value,
                    event_type["value"],
                    start_input.value,
                    end_input.value
                )
            ).classes("event-btn w-64 mt-6")
