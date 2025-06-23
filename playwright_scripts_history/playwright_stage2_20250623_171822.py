import traceback
from playwright_tools.session_context import PlaywrightSessionContext
from playwright_tools.detect_stage_tool import detect_quickdraw_stage

def main():
    try:
        context = PlaywrightSessionContext()
        page = context.get_page()
        state = context.get_state()

        print(f"DEBUG: type(state) = {type(state)}, repr(state) = {repr(state)}")

        try:
            if not isinstance(state, dict):
                raise TypeError("state is not a dict (isinstance check failed)")
        except Exception:
            try:
                if type(state) is not dict:
                    raise TypeError("state is not a dict (type check fallback failed)")
            except Exception as e:
                err_trace = traceback.format_exc()
                print(f"Type check failed for state with fallback: {err_trace}")
                state = {}
                error_log_list = []
                try:
                    error_log_list = state.get("type_check_errors", [])
                    if not isinstance(error_log_list, list):
                        error_log_list = []
                except Exception:
                    error_log_list = []
                error_log_list.append({
                    "error": str(e),
                    "traceback": err_trace,
                    "recovery": "Reinitialized state as empty dict"
                })
                state["type_check_errors"] = error_log_list
                context.save_state()
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
