"""NiceGUI Time Tracker page."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta

import httpx
from nicegui import ui

from frontend.api_client import get_events, get_time_entries
from frontend.theme import apply_global_theme
from frontend.menutheme import add_shared_menu

from frontend.timetracker_ui import (
    build_sections_from_api,
    render_week_timeline_html,
    week_start_sunday,
)


@ui.page('/timetracker')
async def timetracker_page() -> None:
    """Render the Time Tracker page UI wired to backend data."""

    apply_global_theme()
    add_shared_menu()

    state: dict[str, str] = {
        "view": "Day",
        "filter": "All",
    }

    week_start = week_start_sunday(date.today())
    week_start_dt = datetime.combine(week_start, time.min)
    week_end_dt = week_start_dt + timedelta(days=7)

    try:
        events = await get_events(start_after=week_start_dt, start_before=week_end_dt, limit=1000)
        time_entries = await get_time_entries(
            start_after=week_start_dt,
            start_before=week_end_dt,
            limit=1000,
        )
    except (httpx.HTTPError, ValueError) as exc:
        ui.notify(f"Failed to load time tracker data: {exc}")
        events = []
        time_entries = []

    sections_all = build_sections_from_api(
        events=events,
        time_entries=time_entries,
        week_start=week_start,
    )
    filter_options = ["All"] + [s.title for s in sections_all]

    with ui.column().classes("w-full items-center"):
        with ui.row().classes("w-11/12 md:w-2/3 items-center justify-between mt-2"):
            ui.label("").classes("w-8")  # spacer for visual centering
            ui.label("Time Tracker").classes("tt-page-title")
            ui.button(
                icon="mail",
                on_click=lambda: ui.notify("Coming soon"),
            ).props("flat round").classes("tt-mail-btn")

        with ui.column().classes("w-11/12 md:w-2/3 items-center mt-2"):
            with ui.row().classes("w-full items-center justify-center gap-4 tt-controls"):
                ui.toggle(
                    ["Day", "Week", "Month"],
                    value=state["view"],
                    on_change=lambda e: set_view(e.value),
                ).classes("tt-view-toggle")

            with ui.row().classes("w-full items-center justify-center mt-3"):
                ui.select(
                    filter_options,
                    value=state["filter"],
                    on_change=lambda e: set_filter(e.value),
                ).classes("tt-filter w-40")

            view_note = ui.label("").classes("tt-view-note mt-2")

        charts_container = ui.column().classes("w-11/12 md:w-2/3 space-y-6 mt-4 pb-10")

    def _filtered_sections() -> list:
        selection = state["filter"]
        if selection == "All":
            return sections_all
        return [s for s in sections_all if s.title == selection]

    def render() -> None:
        if state["view"] == "Day":
            view_note.set_visibility(False)
        else:
            view_note.set_text(f"{state['view']} view coming soon (showing weekly layout for now)")
            view_note.set_visibility(True)

        charts_container.clear()
        sections = _filtered_sections()
        with charts_container:
            if not sections:
                ui.label("No sections to display").classes("tt-empty-state")
            for section in sections:
                ui.html(render_week_timeline_html(section), sanitize=False).classes("w-full")

    def set_view(value: str) -> None:
        state["view"] = value
        render()

    def set_filter(value: str) -> None:
        state["filter"] = value
        render()

    render()
