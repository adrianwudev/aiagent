
# Selenium Script - Generated on 2025-06-17 16:09:14
# ================================================


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
import time

def slow_type(element, text, delay=0.1):
    element.clear()
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def find_input(driver):
    selectors = [
        ('css', 'textarea[placeholder*="Message"]'),
        ('css', 'div[contenteditable="true"]'),
        ('xpath', '//textarea[contains(@placeholder, "Message")]'),
        ('xpath', '//div[@contenteditable="true"]'),
        ('css', 'input[type="text"]'),
        ('css', 'textarea[aria-label*="Message"]'),
        ('css', 'div[role="textbox"]'),
        ('css', 'input[placeholder*="Ask"]'),
        ('css', 'textarea[placeholder*="Ask"]')
    ]
    for sel_type, sel_val in selectors:
        try:
            if sel_type == 'css':
                elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel_val)))
                if elem.is_displayed():
                    return elem
            elif sel_type == 'xpath':
                elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, sel_val)))
                if elem.is_displayed():
                    return elem
        except (TimeoutException, NoSuchElementException):
            continue
    # Fallback: print all textarea and inputs for debug
    textareas = driver.find_elements(By.TAG_NAME, 'textarea')
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    print(f"Found {len(textareas)} textareas and {len(inputs)} inputs")
    for i, elem in enumerate(textareas + inputs):
        outer_html = elem.get_attribute('outerHTML')
        print(f"Element {i}: {outer_html[:200]}")
    return None

def find_submit_button(driver):
    submit_selectors = [
        ('css', 'button[type="submit"]'),
        ('css', 'button[aria-label*="Send"]'),
        ('css', 'button[data-testid*="send"]'),
        ('css', 'button[aria-label*="Submit"]'),
        ('css', 'button[title*="Send"]'),
        ('css', 'svg[aria-label*="Send"]'),
    ]
    for sel_type, sel_val in submit_selectors:
        try:
            if sel_type == 'css':
                buttons = driver.find_elements(By.CSS_SELECTOR, sel_val)
                for button in buttons:
                    if button.is_displayed() and button.is_enabled():
                        return button
        except NoSuchElementException:
            continue
    return None

def wait_for_response(driver):
    response_selectors = [
        (By.CSS_SELECTOR, 'div[data-testid*="response"]'),
        (By.CSS_SELECTOR, 'div[class*="response"]'),
        (By.CSS_SELECTOR, 'div[class*="message"]'),
        (By.CSS_SELECTOR, 'div[class*="conversation"]'),
        (By.CSS_SELECTOR, 'div[class*="chat"]'),
    ]
    for sel_type, sel_val in response_selectors:
        try:
            elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((sel_type, sel_val)))
            if elem.is_displayed():
                return elem.text.strip()
        except TimeoutException:
            continue
    return None

def main():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get("https://gemini.google.com/app")
    time.sleep(4)  # Wait for page load

    # Scroll to bottom to reveal input box if necessary
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    conversation = []
    for i in range(1, 21):
        input_box = find_input(driver)
        if not input_box:
            print(f"Input box not found on iteration {i}")
            break

        question = f"Creative question number {i}: What is special about the number {i}?"
        try:
            input_box.clear()
            slow_type(input_box, question, delay=0.05)
        except Exception as e:
            print(f"Failed to type question on iteration {i}: {e}")
            break

        # Verify text entered
        try:
            entered_text = input_box.get_attribute('value') or input_box.text
            if question not in entered_text:
                print(f"Typed question not verified on iteration {i}")
                break
        except Exception as e:
            print(f"Error verifying typed text on iteration {i}: {e}")
            break

        # Find submit button
        submit_button = find_submit_button(driver)
        if not submit_button:
            print(f"Submit button not found on iteration {i}")
            break

        # Click submit
        try:
            submit_button.click()
        except Exception as e:
            print(f"Submit click failed on iteration {i}: {e}")
            break

        # Wait for response
        response_text = wait_for_response(driver)
        if not response_text:
            print(f"No response detected on iteration {i}")
            response_text = "(No response detected)"
        conversation.append((question, response_text))
        print(f"Q{i}: {question}")
        print(f"A{i}: {response_text}")
        time.sleep(2)  # small wait before next iteration

    driver.quit()
    return conversation

if __name__ == "__main__":
    conv = main()
    # Format conversation for saving or display
    convo_text = "\n\n".join([f"Q{i+1}: {q}\nA{i+1}: {a}" for i, (q, a) in enumerate(conv)])
    print("Final conversation summary:")
    print(convo_text)


# ================================================
