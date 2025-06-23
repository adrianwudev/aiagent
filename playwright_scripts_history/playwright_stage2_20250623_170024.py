# Playwright script for stage 2

from playwright_tools.detect_stage_tool import detect_quickdraw_stage
from playwright_tools.session_context import PlaywrightSessionContext

state = PlaywrightSessionContext().get_state()
page = PlaywrightSessionContext().get_page()

try:
    current_stage = detect_quickdraw_stage()
    print(f"Current Stage: {current_stage}")

    if not (type(state) is dict):
        state = {}

    if "step_completed" not in state or not (type(state.get("step_completed", None)) is dict):
        state["step_completed"] = {}

    if not state["step_completed"].get("prompt_fetched", False):
        prompt_word = page.eval_on_selector("#challengetext-word", "el => el ? el.innerText.trim() : ''")
        if prompt_word == "":
            print("Prompt element not found or empty on stage 2.")
        else:
            state["prompt_word"] = prompt_word
            state["step_completed"]["prompt_fetched"] = True
            state["stage_2_done"] = True
            state["drawing_plan"] = [
                {"type": "move", "x": 50, "y": 50},
                {"type": "down"},
                {"type": "move", "x": 150, "y": 150},
                {"type": "up"},
            ]
except Exception as e:
    print(e)

PlaywrightSessionContext().save_state()