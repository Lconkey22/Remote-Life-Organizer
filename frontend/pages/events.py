from nicegui import ui
from datetime import datetime

# Store events
calendar_events = []
event_type = {"value": None}

# -------------------------
# SHARED MENU FOR ALL PAGES
# -------------------------
def add_shared_menu():

    # Add global CSS theme once per page load
    ui.add_head_html("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poiret+One&display=swap" rel="stylesheet">

    <style>
        body {
            background: #1B301B;
            font-family: "Poiret One", sans-serif;
        }

        .header-bar {
            background: linear-gradient(90deg, #2E4A3A, #1F3528);
            border-bottom: 2px solid #D9C6A9;
        }

        .drawer-bg {
            background: #F4EDE1 !important;
        }

        .drawer-btn {
            color: #2E4A3A !important;
            font-weight: 600;
        }

        .drawer-btn:hover {
            background: #E6D9C7 !important;
        }

        .signout-btn {
            color: #7a1f1f !important;
            font-weight: bold;
        }

        .events-card {
            background: #F9F5EE;
            border-radius: 18px;
            border: 1.5px solid #D9C6A9;
            box-shadow: 0 6px 16px rgba(0,0,0,0.12);
            padding: 20px;
        }

        .events-title {
            color: #D9C6A9;
            font-size: 30px;
            text-align: center;
            margin-top: 20px;
            margin-bottom: 30px;
        }

        .event-label {
            color: #2E4A3A;
            font-weight: 600;
        }

        .event-btn {
            background: #2E4A3A !important;
            color: white !important;
            border-radius: 10px;
        }

        .event-btn:hover {
            background: #23392E !important;
        }

        .event-input {
            border: 1.5px solid #D9C6A9 !important;
            border-radius: 10px !important;
            background: #FFFDF8 !important;
        }
    </style>
    """)

    # Drawer
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
        ui.button("Profile", on_click=lambda: ui.notify("Profile")).classes("drawer-btn w-full text-left")

        ui.separator().classes("my-4")
        ui.button("Sign Out", on_click=lambda: ui.navigate.to('/login')).classes("signout-btn w-full text-left")

    # Header
    with ui.header().classes("header-bar h-24 text-white relative flex items-center shadow-lg"):
        ui.button(icon="menu", on_click=lambda: drawer.toggle()).classes("text-white mr-4")

        with ui.element("div").classes(
            "absolute left-1/2 -translate-x-1/2 flex flex-col items-center"
        ):
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
# EVENTS PAGE
# -------------------------
@ui.page('/events')
def events_page():
    add_shared_menu()

    ui.label("Add a New Event").classes("events-title")

    with ui.column().classes("items-center space-y-6"):

        # Event Type Buttons (styled)
        ui.button("Work Shift", on_click=lambda: event_type.update(value="Work"))\
            .classes("event-btn w-64")
        ui.button("Family Event", on_click=lambda: event_type.update(value="Family"))\
            .classes("event-btn w-64")
        ui.button("School Event", on_click=lambda: event_type.update(value="School"))\
            .classes("event-btn w-64")
        ui.button("Other Event", on_click=lambda: event_type.update(value="Other"))\
            .classes("event-btn w-64")

        # Card layout
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
