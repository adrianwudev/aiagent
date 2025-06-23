from smolagents.tools import tool
from playwright_tools.session_context import PlaywrightSessionContext

@tool
def read_prompt_tool() -> str:
    """
    name=read_prompt_tool
    Extract the current drawing prompt word from the Quick, Draw! game page.
    This tool scans the #challengetext-word div and concatenates the innerText of all its child spans to reconstruct the prompt word.
    Returns:
        str: The prompt word (e.g., 'alarm clock'), or an error message if not found.
    """
    page = PlaywrightSessionContext().get_page()
    div = page.query_selector('#challengetext-word')
    if not div:
        return "Prompt div (#challengetext-word) not found."
    spans = div.query_selector_all('span')
    if not spans:
        return "No spans found in #challengetext-word."
    word = ''.join([span.inner_text() for span in spans])
    return word.strip() 