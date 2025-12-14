"""NiceGUI Calendar page wired to the backend Events API."""

from __future__ import annotations

from datetime import date, datetime, time

import httpx
from nicegui import ui

from frontend.theme import apply_global_theme
from frontend.menutheme import add_shared_menu
from frontend import api_client

# -------------------------
# CALENDAR PAGE  (/calendar)
# -------------------------
@ui.page('/calendar')
async def events_page() -> None:
    """Render the calendar and fetch events for the selected day."""
    apply_global_theme()
    add_shared_menu()

    ui.label("Calendar").classes("events-title")

    with ui.column().classes("items-center space-y-6"):

        # Date selection card
        with ui.card().classes("events-card w-11/12 md:w-2/3"):
            ui.label("Select a date").classes("event-label mb-1")
            selected_date = ui.date().classes("w-full")

        # Events display card
        events_card = ui.card().classes("events-card w-11/12 md:w-2/3")

        async def refresh_events_display() -> None:
            events_card.clear()
            with events_card:
                if not selected_date.value:
                    ui.label("Please select a date to view events").classes(
                        "text-gray-500 italic"
                    )
                    return

                ui.label("Loading…").classes("text-gray-500 italic")

            try:
                day = date.fromisoformat(str(selected_date.value))
            except ValueError:
                events_card.clear()
                with events_card:
                    ui.label("Invalid date selected").classes("text-gray-500 italic")
                return

            start_after = datetime.combine(day, time.min)
            start_before = datetime.combine(day, time.max)

            try:
                events = await api_client.get_events(
                    start_after=start_after,
                    start_before=start_before,
                    limit=1000,
                    offset=0,
                )
            except httpx.HTTPError as exc:
                ui.notify(f"Failed to load events: {exc}", color="red")
                events_card.clear()
                with events_card:
                    ui.label("Failed to load events").classes("text-gray-500 italic")
                return

            events_card.clear()
            with events_card:
                ui.label(f"Events for {day.isoformat()}").classes("event-label mb-4")

                if events:
                    for event in events:
                        with ui.row().classes(
                            "items-center mb-3 p-2 border-b border-gray-200"
                        ):
                            ui.label(f"{event['name']}").classes("font-semibold mr-4")
                            ui.label(f"Type: {event['type']}").classes(
                                "text-gray-600 mr-4"
                            )
                            start_time = datetime.fromisoformat(event["start_time"])
                            end_time = datetime.fromisoformat(event["end_time"])
                            time_range = (
                                f"{start_time.strftime('%I:%M %p')} - "
                                f"{end_time.strftime('%I:%M %p')}"
                            )
                            ui.label(
                                time_range
                            ).classes("text-gray-500")
                else:
                    ui.label("No events for this date").classes("text-gray-500 italic")

        async def _on_date_change(_e) -> None:
            await refresh_events_display()

        # Update events when date changes
        selected_date.on("update:modelValue", _on_date_change)

        # Initial display
        await refresh_events_display()
