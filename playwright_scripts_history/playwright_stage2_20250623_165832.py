# Playwright script for stage 2

import traceback
from playwright_tools.detect_stage_tool import detect_quickdraw_stage
from playwright_tools.session_context import PlaywrightSessionContext
from playwright.sync_api import TimeoutError

state = PlaywrightSessionContext().get_state()
page = PlaywrightSessionContext().get_page()

try:
    current_stage = detect_quickdraw_stage()
    print(f"Current Stage: {current_stage}")

    if not isinstance(state, dict):
        state = {}
    if "step_completed" not in state or not isinstance(state.get("step_completed", None), dict):
        state["step_completed"] = {}

    if current_stage == 3:
        if not state["step_completed"].get("stage_3_clicked", False):
            got_it_button = page.locator('text="Got It!"')
            got_it_button.wait_for(state="visible", timeout=5000)
            got_it_button.click()
            state["step_completed"]["stage_3_clicked"] = True
            state["stage_3_done"] = True
    else:
        print(f"Current stage is {current_stage}, expected stage 3.")

except Exception as e:
    print(traceback.format_exc())

PlaywrightSessionContext().save_state()