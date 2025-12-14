"""NiceGUI page for creating events."""

from datetime import date, datetime, time

from nicegui import ui

from frontend.theme import apply_global_theme
from frontend.menutheme import add_shared_menu
from frontend import api_client

EVENT_TYPE_OPTIONS = ["Work", "Family", "School", "Other"]


def _time_options_15m() -> list[str]:
    """Generate 12-hour time strings in 15-minute increments."""
    options: list[str] = []
    for minutes in range(0, 24 * 60, 15):
        hours, mins = divmod(minutes, 60)
        value = datetime(2000, 1, 1, hours, mins).strftime("%I:%M %p").lstrip("0")
        options.append(value)
    return options


TIME_OPTIONS_15M = _time_options_15m()


def _parse_date(value: str | None) -> date | None:
    """Parse a YYYY-MM-DD date string into a `date`."""
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _parse_time(value: str | None) -> time | None:
    """Parse a user-entered time string like '1:30 PM' into a `time`."""
    if not value:
        return None
    try:
        return datetime.strptime(value.strip().upper(), "%I:%M %p").time()
    except ValueError:
        return None


# -------------------------
# EVENTS PAGE  (/events)
# -------------------------
@ui.page('/events')
def events_page():
    """Render the Add Event form and persist via the backend API."""
    apply_global_theme()
    add_shared_menu()

    ui.label("Add a New Event").classes("events-title")

    with ui.column().classes("items-center space-y-6"):

        name_input = ui.input(label="Event name").classes("event-input w-64")
        type_select = ui.select(
            options=EVENT_TYPE_OPTIONS,
            label="Event type",
            value=None,
        ).classes("event-input w-64")

        # Event input card
        with ui.card().classes("events-card w-11/12 md:w-2/3"):

            ui.label("Select a date").classes("event-label mb-1")
            selected_date = ui.date().classes("w-full")

            ui.separator().classes("my-4")

            ui.label("Start time").classes("event-label")
            start_select = ui.select(options=TIME_OPTIONS_15M, value=None).classes(
                "event-input w-64"
            )

            ui.label("End time").classes("event-label mt-3")
            end_select = ui.select(options=TIME_OPTIONS_15M, value=None).classes(
                "event-input w-64"
            )

            async def _save_event() -> None:
                name = (name_input.value or "").strip()
                event_type = type_select.value
                day = _parse_date(selected_date.value)
                start_time = _parse_time(start_select.value)
                end_time = _parse_time(end_select.value)

                if (
                    not name
                    or not event_type
                    or day is None
                    or start_time is None
                    or end_time is None
                ):
                    ui.notify("All fields required", color="red")
                    return

                start_dt = datetime.combine(day, start_time)
                end_dt = datetime.combine(day, end_time)
                if end_dt <= start_dt:
                    ui.notify("End time must be after start time", color="red")
                    return

                try:
                    await api_client.create_event(
                        name=name,
                        type_=event_type,
                        start_time=start_dt,
                        end_time=end_dt,
                    )
                except Exception as exc:  # pylint: disable=broad-exception-caught
                    ui.notify(f"Failed to save event: {exc}", color="red")
                    return

                ui.notify("Event Added!", color="green")
                name_input.value = ""
                type_select.value = None
                start_select.value = None
                end_select.value = None

            ui.button("Save Event", on_click=_save_event).classes("event-btn w-64 mt-6")
