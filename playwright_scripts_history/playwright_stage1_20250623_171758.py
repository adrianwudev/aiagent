import traceback
from playwright_tools.session_context import PlaywrightSessionContext
from playwright_tools.detect_stage_tool import detect_quickdraw_stage

def main():
    try:
        context = PlaywrightSessionContext()
        page = context.get_page()
        state = context.get_state()
        if not isinstance(state, dict):
            state = {}
    except Exception as e:
        print(f"Error initializing PlaywrightSessionContext or state: {e}")
        state = {}
        context = PlaywrightSessionContext()
        page = context.get_page()

    try:
        stage = detect_quickdraw_stage()
        print(f"Detected stage: {stage}")
    except Exception:
        stage = 0

    if stage == 1:
        if not state.get("stage_1_completed", False):
            button = page.query_selector("button:has-text(\"Let's Draw!\")")
            if button is not None:
                button.click()
                state["stage_1_completed"] = True
                context.save_state()

if __name__ == "__main__":
    main()
