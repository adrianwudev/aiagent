# ===
# Goal: Click the "Let's Draw!" button to start the game (step 1)
# Achieved: Yes
# Reason for Failure: N/A
# Suggestions for Improvement: Ensure button text is stable and handle timeouts better.
# ===

from playwright_tools.session_context import PlaywrightSessionContext

page = PlaywrightSessionContext().get_page()
button = page.wait_for_selector("button:has-text(\"Let's Draw!\")", timeout=10000)
button.click()

state = PlaywrightSessionContext().get_state()
if not state:
    state = {}
state['current_step'] = 1
PlaywrightSessionContext().save_state()
