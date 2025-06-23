# ===
# Goal: Draw a simple snowflake shape on canvas within 20 seconds (step 6)
# Achieved: Yes
# Reason for Failure: N/A
# Suggestions for Improvement: Enhance drawing with detailed strokes based on tutorial.
# ===

from playwright_tools.session_context import PlaywrightSessionContext
import time

page = PlaywrightSessionContext().get_page()
canvas = page.wait_for_selector("canvas", timeout=10000)
box = canvas.bounding_box()
center_x = box['x'] + box['width'] / 2
center_y = box['y'] + box['height'] / 2

page.mouse.move(center_x, center_y - 100)
page.mouse.down()
page.mouse.move(center_x, center_y + 100, steps=20)
page.mouse.up()

page.mouse.move(center_x - 100, center_y)
page.mouse.down()
page.mouse.move(center_x + 100, center_y, steps=20)
page.mouse.up()

page.mouse.move(center_x - 70, center_y - 70)
page.mouse.down()
page.mouse.move(center_x + 70, center_y + 70, steps=20)
page.mouse.up()

page.mouse.move(center_x - 70, center_y + 70)
page.mouse.down()
page.mouse.move(center_x + 70, center_y - 70, steps=20)
page.mouse.up()

time.sleep(1)

state = PlaywrightSessionContext().get_state()
if not state:
    state = {}
state['current_step'] = 6
PlaywrightSessionContext().save_state()
