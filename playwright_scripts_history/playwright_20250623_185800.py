# ===
# Goal: Wait for the drawing canvas to be ready (step 5)
# Achieved: Yes
# Reason for Failure: N/A
# Suggestions for Improvement: Add retry logic if canvas not ready within timeout.
# ===

from playwright_tools.session_context import PlaywrightSessionContext

page = PlaywrightSessionContext().get_page()
canvas = page.wait_for_selector("canvas", timeout=15000)

state = PlaywrightSessionContext().get_state()
if not state:
    state = {}
state['current_step'] = 5
PlaywrightSessionContext().save_state()
