"""NiceGUI Home page (dashboard)."""

from __future__ import annotations

from nicegui import ui

import httpx

from frontend import api_client
from frontend.theme import apply_global_theme
from frontend.menutheme import add_shared_menu


# -------------------------
# HOME PAGE  (/home)
# -------------------------
@ui.page('/home')
async def home_page() -> None:
    """Render the dashboard with upcoming events grouped by category."""
    apply_global_theme()
    add_shared_menu()

    data = await api_client.get_homepage()

    events = data["events"]

    ui.label("Your Dashboard").classes("home-title text-center mt-6")

    categories = ["Family", "Homework", "Work", "Other"]
    with ui.column().classes("p-4 items-center space-y-8 w-full"):
        for category in categories:
            with ui.card().classes("w-96 h-64 overflow-auto border-2 border-gray-300"):
                ui.label(f"Upcoming {category} Events").classes(
                    "text-xl font-bold mb-2 border-b-2 border-gray-400 pb-1"
                )

                filtered_events = [event for event in events if event["type"] == category]

                if filtered_events:
                    for event in filtered_events:
                        event_id = event.get("id")
                        is_completed = bool(event.get("completed", False))

                        with ui.row().classes("items-center mb-1 space-x-2"):
                            label = ui.label(
                                f"{event['name']}: {event['start_time']}"
                            )

                            if is_completed:
                                label.classes(add="line-through")

                            async def _on_toggle(
                                e,
                                *,
                                ev=event,
                                ev_id=event_id,
                                lbl=label,
                            ) -> None:
                                cb = e.sender
                                if ev_id is None:
                                    ui.notify(
                                        "Event is missing an id; cannot update completion.",
                                        color="red",
                                    )
                                    cb.value = bool(ev.get("completed", False))
                                    return

                                previous = bool(ev.get("completed", False))
                                requested = bool(e.value)

                                try:
                                    updated = await api_client.set_event_completed(ev_id, requested)
                                except httpx.HTTPError as exc:
                                    ui.notify(
                                        f"Failed to update event completion: {exc}",
                                        color="red",
                                    )
                                    cb.value = previous
                                    if previous:
                                        lbl.classes(add="line-through")
                                    else:
                                        lbl.classes(remove="line-through")
                                    return

                                ev["completed"] = bool(updated.get("completed", requested))
                                if ev["completed"]:
                                    lbl.classes(add="line-through")
                                else:
                                    lbl.classes(remove="line-through")

                            ui.checkbox(value=is_completed, on_change=_on_toggle)

                else:
                    ui.label("No upcoming events")
