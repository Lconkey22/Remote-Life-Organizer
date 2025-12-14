"""NiceGUI Time Tracker page (frontend-only, demo data)."""

from nicegui import ui
from frontend.theme import apply_global_theme
from frontend.menutheme import add_shared_menu

from frontend.timetracker_ui import get_demo_sections, render_week_timeline_html


@ui.page('/timetracker')
def timetracker_page():
    """Render the Time Tracker page UI (not yet wired to backend)."""

    apply_global_theme()
    add_shared_menu()

    state: dict[str, str] = {
        "view": "Day",
        "filter": "All",
    }

    demo_sections = get_demo_sections()

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
                    ["All", "Work/School", "Homework", "Self Care"],
                    value=state["filter"],
                    on_change=lambda e: set_filter(e.value),
                ).classes("tt-filter w-40")

            view_note = ui.label("").classes("tt-view-note mt-2")

        charts_container = ui.column().classes("w-11/12 md:w-2/3 space-y-6 mt-4 pb-10")

    def _filtered_sections() -> list:
        selection = state["filter"]
        if selection == "All":
            return demo_sections
        return [s for s in demo_sections if s.title == selection]

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
