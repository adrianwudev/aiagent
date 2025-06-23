# Playwright script for stage 2

from playwright_tools.detect_stage_tool import detect_quickdraw_stage
from playwright_tools.session_context import PlaywrightSessionContext

def draw_plan_on_canvas(drawing_plan, page):
    try:
        canvas = page.locator("canvas")
        canvas.bounding_box()  # Check canvas

        for action in drawing_plan:
            if type(action) is dict:
                t = action.get("type")
                if t == "move":
                    page.mouse.move(action.get("x", 0), action.get("y", 0))
                elif t == "down":
                    page.mouse.down()
                elif t == "up":
                    page.mouse.up()
        return True
    except Exception as e:
        print("Exception during drawing:", e)
        return False

state = PlaywrightSessionContext().get_state()
page = PlaywrightSessionContext().get_page()

try:
    current_stage = detect_quickdraw_stage()
    print(f"Current Stage: {current_stage}")

    if type(state) is not dict:
        state = {}
    if "step_completed" not in state or type(state.get("step_completed")) is not dict:
        state["step_completed"] = {}

    if current_stage == 4:
        if not state.get("drawing_done", False):
            drawing_plan = state.get("drawing_plan")
            if type(drawing_plan) is list and len(drawing_plan) > 0:
                draw_plan_on_canvas(drawing_plan, page)
                state["drawing_done"] = True
except Exception as e:
    print(e)

PlaywrightSessionContext().save_state()