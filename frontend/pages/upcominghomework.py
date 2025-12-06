# -------------------------
# UPCOMING HOMEWORK PAGE  (/homework)
# -------------------------
from nicegui import ui
from frontend.theme import apply_global_theme
from frontend.add_shared_menu import add_shared_menu 

@ui.page('/upcominghomework')
def upcoming_homework_page():
    apply_global_theme()
    add_shared_menu()

    # Page title
    ui.label("Upcoming Homework").classes("home-title text-center mt-6 text-[#2E4A3A]")

    # Container for homework items
    homework_list = []

    homework_column = ui.column().classes("p-4 items-center space-y-6 w-full")  # cards go here

    # -------------------------
    # Form to add new homework
    # -------------------------
    with ui.card().classes("w-10/12 md:w-2/3 lg:w-1/2 p-4 mb-4"):
        ui.label("Add New Homework").classes("text-lg font-bold text-[#2E4A3A] mb-2")

        course_input = ui.input(label="Course Name").classes("w-full")
        due_input = ui.input(label="Due Date (YYYY-MM-DD)").classes("w-full")
        desc_input = ui.textarea(label="Description").classes("w-full")

        def add_homework():
            hw = {
                "course": course_input.value,
                "due_date": due_input.value,
                "description": desc_input.value
            }
            homework_list.append(hw)
            render_homework()
            # Clear inputs
            course_input.set_value("")
            due_input.set_value("")
            desc_input.set_value("")
            ui.notify(f"Homework for {hw['course']} added!")

        ui.button("Add Homework", on_click=add_homework).classes("mt-2 bg-[#2E4A3A] text-white hover:bg-[#3E5A4A]")

    # -------------------------
    # Function to render homework cards
    # -------------------------
    def render_homework():
        homework_column.clear()  # remove old cards
        for hw in homework_list:
            with homework_column:
                with ui.card().classes("home-card w-10/12 md:w-2/3 lg:w-1/2 p-4"):
                    ui.label(hw["course"]).classes("text-xl font-bold mb-1 text-[#2E4A3A]")
                    ui.label(f"Due Date: {hw['due_date']}").classes("text-sm text-gray-500 mb-2")
                    ui.label(hw["description"]).classes("item-text")
                    ui.button(
                        "Mark as Done",
                        on_click=lambda hw=hw: homework_done(hw)
                    ).classes("mt-2 bg-[#2E4A3A] text-white hover:bg-[#3E5A4A]")

    # -------------------------
    # Function to mark homework as done
    # -------------------------
    def homework_done(hw):
        if hw in homework_list:
            homework_list.remove(hw)
            render_homework()
            ui.notify(f"{hw['course']} marked as done!")
