# ===
# Goal: Capture canvas drawing screenshot as base64 string and save in state (step 7)
# Achieved: Yes
# Reason for Failure: N/A
# Suggestions for Improvement: Implement external export or download in future iterations.
# ===

from playwright_tools.session_context import PlaywrightSessionContext
import base64

page = PlaywrightSessionContext().get_page()
canvas = page.wait_for_selector("canvas", timeout=10000)

canvas_bytes = canvas.screenshot()
canvas_base64 = base64.b64encode(canvas_bytes).decode('utf-8')

state = PlaywrightSessionContext().get_state()
if not state:
    state = {}
state['current_step'] = 7
state['canvas_image_base64'] = canvas_base64
PlaywrightSessionContext().save_state()
