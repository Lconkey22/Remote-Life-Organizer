from nicegui import ui
from datetime import datetime

# ----------------------------------
# GLOBAL CALENDAR DATA
# ----------------------------------
calendar_events = []
event_type = {"value": None}


# ----------------------------------
# SHARED MENU FOR ALL INTERNAL PAGES
# ----------------------------------
def add_shared_menu():

    drawer = ui.left_drawer(value=False).classes("bg-white")
    with drawer:
        ui.label("Menu").classes("text-xl font-bold p-4")
        ui.separator()

        ui.button("Home", on_click=lambda: ui.navigate.to("/home"))
        ui.button("Upcoming Events", on_click=lambda: ui.notify("Upcoming Events"))
        ui.button("Upcoming Homework", on_click=lambda: ui.notify("Upcoming Homework"))
        ui.button("Calendar", on_click=lambda: ui.notify("Calendar"))
        ui.button("Add Events", on_click=lambda: ui.navigate.to("/events"))
        ui.button("Time Tracker", on_click=lambda: ui.notify("Time Tracker"))

        ui.separator().classes("my-3")
        for name in ["Settings", "Profile+", "Search", "Help"]:
            ui.button(name, on_click=lambda n=name: ui.notify(n)).classes(
                "w-full text-left py-2"
            )

        ui.separator().classes("my-4")
        ui.button("Profile", on_click=lambda: ui.notify("Profile")).classes("w-full text-left")

        ui.separator().classes("my-4")
        ui.button("Sign Out", on_click=lambda: ui.navigate.to('/login')).classes(
            "w-full text-left text-red-600"
        )

    # HEADER
    with ui.header().classes("h-24 bg-blue-600 text-white flex items-center"):
        ui.button(icon="menu", on_click=lambda: drawer.toggle()).classes("text-white")

        with ui.element("div").classes("ml-auto mr-4 flex flex-col items-center"):
            with ui.element("div").classes("w-12 h-12 rounded-full overflow-hidden"):
                ui.image("profile_picture_example.jpg").classes("w-full h-full object-cover")
            ui.label("Hello, Username").classes("text-lg font-semibold mt-2")


# ----------------------------------
# EVENT CREATION
# ----------------------------------
def create_event(selected_date, event_type_name, start_time_str, end_time_str):

    if not selected_date:
        ui.notify("No date selected", color="red")
        return
    if not event_type_name:
        ui.notify("No event type selected", color="red")
        return
    if not start_time_str:
        ui.notify("No start time entered", color="red")
        return
    if not end_time_str:
        ui.notify("No end time entered", color="red")
        return

    try:
        datetime.strptime(start_time_str.strip(), "%I:%M %p")
    except ValueError:
        ui.notify("Invalid START time. Use HH:MM AM/PM", color="red")
        return

    try:
        datetime.strptime(end_time_str.strip(), "%I:%M %p")
    except ValueError:
        ui.notify("Invalid END time. Use HH:MM AM/PM", color="red")
        return

    calendar_events.append({
        "type": event_type_name,
        "date": selected_date,
        "start time": start_time_str.upper(),
        "end time": end_time_str.upper()
    })

    ui.notify(
        f"{event_type_name} event added on {selected_date} "
        f"from {start_time_str.upper()} to {end_time_str.upper()}",
        color="green"
    )


# ----------------------------------
# EVENTS PAGE 
# ----------------------------------
@ui.page("/events")
def events_page():

    add_shared_menu()

    with ui.column().classes("p-4 items-center space-y-6"):
        ui.button("Add Work Shift", on_click=lambda: (
            event_type.update(value="Work"),
            ui.notify("Selected event: Work")
        )).classes("w-64 text-xl font-bold")

        ui.button("Add Family Event", on_click=lambda: (
            event_type.update(value="Family"),
            ui.notify("Selected event: Family")
        )).classes("w-64 text-xl font-bold")

        ui.button("Add School Event", on_click=lambda: (
            event_type.update(value="School"),
            ui.notify("Selected event: School")
        )).classes("w-64 text-xl font-bold")

        ui.button("Add Other Event", on_click=lambda: (
            event_type.update(value="Other"),
            ui.notify("Selected event: Other")
        )).classes("w-64 text-xl font-bold")

        ui.separator()

        ui.label("Select a date").classes("text-lg font-bold mb-2")
        selected_date = ui.date().classes("w-full")

        ui.label().bind_text_from(selected_date, "value", lambda v: f"You selected: {v}")

        ui.label("Enter start time (HH:MM AM/PM)").classes("text-lg font-bold mt-4")
        start_time_input = ui.input(placeholder="EX: 7:30 PM").classes("w-64")

        ui.label("Enter end time (HH:MM AM/PM)").classes("text-lg font-bold mt-4")
        end_time_input = ui.input(placeholder="EX: 9:00 PM").classes("w-64")

        ui.button(
            "Save Event",
            on_click=lambda: create_event(
                selected_date.value,
                event_type["value"],
                start_time_input.value,
                end_time_input.value
            ),
        ).classes("w-64 bg-green-500 text-white mt-4")


# ----------------------------------
# RUN APP
# ----------------------------------
ui.run()
