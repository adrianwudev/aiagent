from playwright_tools.session_context import PlaywrightSessionContext

def run_stage_1_click():
    context = PlaywrightSessionContext()
    page = context.get_page()
    button = page.locator("text=Let's Draw!")
    button.wait_for(state="visible", timeout=5000)
    button.click()
    state = context.get_state()
    if type(state.get('completed_steps')) is not dict:
        state['completed_steps'] = {}
    state['completed_steps']['stage_1_clicked'] = True
    context.save_state()

run_stage_1_click()
