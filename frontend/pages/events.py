from nicegui import ui
from datetime import datetime

# Note - Relevant Tailwind CSS Utility Classes documentation can be found here: https://tailwind.build/classes

# Creates calendar_events list that will store all created events
# event_type dictionary stores relevant information for every event
calendar_events = []
event_type = {"value": None}

# Function used to created event_type dictionary elements, with user-input validation
def create_event(selected_date, event_type_name, start_time_str, end_time_str):
    """Creates event based on selected date and event type"""
    # Input validation to ensure all relevant variables
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

    # Validates start time using try-except statements
    try:
        # .strip removes all spaces around time string
        # strptime converts string variable to datetime object
        # %I (12-hour clock), %M (Minutes 00-59), %p (AM or PM)
        # More information about Python datetime here: https://docs.python.org/3/library/datetime.html
        datetime.strptime(start_time_str.strip(), "%I:%M %p")
    # If try fails (time is in improper format) this except is executed
    except ValueError:
        ui.notify("Invalid START time. Use HH:MM AM/PM (ex: 7:30 PM)", color="red")
        return

    # Validates end time (same format as above)
    try:
        datetime.strptime(end_time_str.strip(), "%I:%M %p")
    except ValueError:
        ui.notify("Invalid END time. Use HH:MM AM/PM (ex: 9:00 PM)", color="red")
        return

    # Saves event data using dictionary and appends it to calendar_events list
    calendar_events.append({
        "type": event_type_name,
        "date": selected_date,
        "start time": start_time_str.upper(),
        "end time": end_time_str.upper()
    })

    # Notifies user that event was successfully added
    ui.notify(
        f"{event_type_name} event added on {selected_date} from {start_time_str.upper()} to {end_time_str.upper()}",
        color="green"
    )


# Home Page
@ui.page("/")
def home_page():
    # Creates "hamburger menu"
    # .left_drawer creates side menu that is on the left of the screen
    # and can be opened by the user (value = False so it is normally closed)
    drawer = ui.left_drawer(value=False).classes("bg-white")

    # with statement defines parent-child relationships between UI elements
    with drawer:
        ui.label("Menu").classes("text-xl font-bold p-4")
        ui.separator()
        ui.button("Home", on_click=lambda: ui.notify("Home"))
        ui.button("Upcoming Events", on_click=lambda: ui.notify("Upcoming Events"))
        ui.button("Upcoming Homework", on_click=lambda: ui.notify("Upcoming Homework"))
        ui.button("Calendar", on_click=lambda: ui.notify("Calendar"))
        ui.button("Add Events", on_click=lambda: ui.navigate.to("/add-events"))
        ui.button("Time Tracker", on_click=lambda: ui.notify("Time Tracker"))
        ui.separator().classes("my-3")

        # Notifies user when any of the following buttons are pressed
        for name in ["Settings", "Profile+", "Search", "Help"]:
            ui.button(name, on_click=lambda n=name: ui.notify(n)).classes("w-full text-left py-2")

        # Creates line to separate UI elements for organizational purposes
        ui.separator().classes("my-4")
        ui.button("Profile", on_click=lambda: ui.notify("Profile")).classes("w-full text-left")

    # Creates top blue header with user-name and profile picture
    with ui.header().classes("h-24 bg-blue-600 text-white relative flex items-center"):
        ui.button(icon="menu", on_click=lambda: drawer.toggle()).classes("text-white")
        with ui.element("div").classes("absolute left-1/2 -translate-x-1/2 flex flex-col items-center"):
            with ui.element("div").classes("w-12 h-12 rounded-full overflow-hidden"):
                ui.image("profile_picture_example.jpg").classes("w-full h-full object-cover")
            ui.label("Hello, Username").classes("text-lg font-semibold mt-2")

    # Creates 3 data cards (To be filled later with features not yet implemented)
    with ui.column().classes("p-4 items-center space-y-6"):
        for i in range(1, 4):
            with ui.card().classes("w-96 h-64 overflow-auto border-2 border-gray-300"):
                ui.label(f"Data Block {i}").classes("text-xl font-bold mb-2")
                for j in range(20):
                    ui.label(f"Item {j + 1} in block {i}")


# Add Events Page
@ui.page("/add-events")
def add_events():
    # Creates same "hamburger menu" that appears on the home page
    drawer = ui.left_drawer(value=False).classes("bg-white")
    with drawer:
        ui.label("Menu").classes("text-xl font-bold p-4")
        ui.separator()
        ui.button("Home", on_click=lambda: ui.navigate.to("/"))
        ui.button("Upcoming Events", on_click=lambda: ui.notify("Upcoming Events"))
        ui.button("Upcoming Homework", on_click=lambda: ui.notify("Upcoming Homework"))
        ui.button("Calendar", on_click=lambda: ui.notify("Calendar"))
        ui.button("Add Events", on_click=lambda: ui.navigate.to("/add-events"))
        ui.button("Time Tracker", on_click=lambda: ui.notify("Time Tracker"))

        ui.separator().classes("my-3")
        for name in ["Settings", "Profile+", "Search", "Help"]:
            ui.button(name, on_click=lambda n=name: ui.notify(n)).classes("w-full text-left py-2")

        ui.separator().classes("my-4")
        ui.button("Profile", on_click=lambda: ui.notify("Profile")).classes("w-full text-left")

    with ui.header().classes("h-24 bg-blue-600 text-white relative flex items-center"):
        ui.button(icon="menu", on_click=lambda: drawer.toggle()).classes("text-white")
        with ui.element("div").classes("ml-auto mr-4 flex flex-col items-center"):
            with ui.element("div").classes("w-12 h-12 rounded-full overflow-hidden"):
                ui.image("profile_picture_example.jpg").classes("w-full h-full object-cover")
            ui.label("Hello, Username").classes("text-lg font-semibold mt-2")

    # Creates Row of UI elements that allow the user to select the type
    # of event, the date of the event, the start and end time of the event,
    # and to save the event.
    # The options selected by the user in this portion of the code
    # will save for a call back to the create_event function to store the relevant data
    # when save button is selected by the user
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

        ui.label().bind_text_from(selected_date, 'value', lambda v: f"You selected: {v}")

        # ----- START TIME INPUT -----
        ui.label("Enter start time (HH:MM AM/PM)").classes("text-lg font-bold mt-4")
        start_time_input = ui.input(
            placeholder="EX: 7:30 PM"
        ).classes("w-64")

        # ----- END TIME INPUT -----
        ui.label("Enter end time (HH:MM AM/PM)").classes("text-lg font-bold mt-4")
        end_time_input = ui.input(
            placeholder="EX: 9:00 PM"
        ).classes("w-64")

        # Save button (Calls back to create_event function)
        ui.button(
            "Save Event",
            on_click=lambda: create_event(
                selected_date.value,
                event_type["value"],
                start_time_input.value,
                end_time_input.value
            ),
        ).classes("w-64 bg-green-500 text-white mt-4")

# Runs program
ui.run()
