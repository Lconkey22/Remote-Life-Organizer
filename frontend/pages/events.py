from nicegui import ui
from datetime import datetime

from frontend.theme import apply_global_theme
from frontend.menutheme import add_shared_menu 

# Store events
calendar_events = []
event_type = {"value": None}


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
