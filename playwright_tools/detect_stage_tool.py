from playwright_tools.session_context import PlaywrightSessionContext

# Returns the current Quick, Draw! stage as an integer:
# 1 = Home page (Let's Draw! button visible)
# 2 = Got It! button visible (ready to enter drawing stage)
# 4 = Drawing canvas (whiteboard) visible
# 0 = Unknown or initial state

def detect_quickdraw_stage():
    page = PlaywrightSessionContext().get_page()
    # Only return 4 if both canvas and #clock-time are present (drawing phase)
    canvas = page.query_selector("canvas")
    timer = page.query_selector("#clock-time")
    if canvas and timer and timer.is_visible():
        return 4  # Drawing stage (canvas and timer visible)
    # Only return 2 if 'Got It!' button is visible
    got_it_btn = page.query_selector("text=Got It!") or page.query_selector("button:has-text('Got It!')")
    if got_it_btn and got_it_btn.is_visible():
        return 2  # Got It! button visible
    lets_draw_btn = page.query_selector("text=Let's Draw!") or page.query_selector("button:has-text(\"Let's Draw!\")")
    if lets_draw_btn and lets_draw_btn.is_visible():
        return 1  # Home page, Let's Draw! button visible
    # If unknown, reload homepage and re-detect
    page.goto("https://quickdraw.withgoogle.com/")
    canvas = page.query_selector("canvas")
    timer = page.query_selector("#clock-time")
    if canvas and timer and timer.is_visible():
        return 4
    got_it_btn = page.query_selector("text=Got It!") or page.query_selector("button:has-text('Got It!')")
    if got_it_btn and got_it_btn.is_visible():
        return 2
    lets_draw_btn = page.query_selector("text=Let's Draw!") or page.query_selector("button:has-text(\"Let's Draw!\")")
    if lets_draw_btn and lets_draw_btn.is_visible():
        return 1
    return 0  # Still unknown after reload 