# ===
# Goal: Click the "Got It!" button to enter drawing stage (step 4)
# Achieved: Yes
# Reason for Failure: N/A
# Suggestions for Improvement: Handle alternate wording or button absence gracefully.
# ===

from playwright_tools.session_context import PlaywrightSessionContext

page = PlaywrightSessionContext().get_page()
got_it_button = page.wait_for_selector("button:has-text('Got It!')", timeout=15000)
got_it_button.click()

state = PlaywrightSessionContext().get_state()
if not state:
    state = {}
state['current_step'] = 4
PlaywrightSessionContext().save_state()
