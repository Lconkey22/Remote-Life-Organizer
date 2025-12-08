from nicegui import ui
from frontend.theme import apply_global_theme
from frontend.menutheme import add_shared_menu 


# -------------------------
# HOME PAGE  (/home)
# -------------------------
@ui.page('/home')
async def home_page():
    apply_global_theme()
    add_shared_menu()

    data = await get_homepage()

    tasks = data['tasks']
    events = data['events']
    notifications = data['notifications']

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
                        event.setdefault("completed", False)

                        with ui.row().classes("items-center mb-1 space-x-2"):
                            label = ui.label(
                                f"{event['name']}: {event['start_time']}"
                            )

                            label.classes("line-through" if event["completed"] else "")

                            def make_callback(ev, lbl):
                                def cb(value):
                                    ev["completed"] = value
                                    lbl.classes('line-through' if value else '')

                                return cb

                            ui.checkbox(
                                value = event["completed"],
                                on_change = make_callback(event, label)
                            )

                else:
                    ui.label("No upcoming events")

