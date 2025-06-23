import traceback
from playwright_tools.session_context import PlaywrightSessionContext

def main_error_handling():
    context = PlaywrightSessionContext()
    try:
        raise Exception('Simulated failure in main')
    except Exception as exc:
        print('Error:', exc)
        traceback.print_exc()
    finally:
        context.save_state()

main_error_handling()
