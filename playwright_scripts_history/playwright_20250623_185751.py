# ===
# Goal: Retrieve the drawing prompt from #challengetext-word div (step 2)
# Achieved: Yes
# Reason for Failure: N/A
# Suggestions for Improvement: Add fallback if element not found within timeout.
# ===

from playwright_tools.session_context import PlaywrightSessionContext

page = PlaywrightSessionContext().get_page()
prompt_element = page.wait_for_selector("#challengetext-word", timeout=15000)
prompt_text = prompt_element.inner_text().strip()

state = PlaywrightSessionContext().get_state()
if not state:
    state = {}
state['current_step'] = 2
state['prompt'] = prompt_text
PlaywrightSessionContext().save_state()
