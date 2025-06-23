# ===
# Goal: Initialize Playwright session and open https://quickdraw.withgoogle.com/ (step 0)
# Achieved: Yes
# Reason for Failure: N/A
# Suggestions for Improvement: N/A
# ===

from playwright_tools.session_context import PlaywrightSessionContext

PlaywrightSessionContext().init_session()

state = PlaywrightSessionContext().get_state()
if not state:
    state = {}
state['current_step'] = 0
PlaywrightSessionContext().save_state()
