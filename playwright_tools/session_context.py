from playwright.sync_api import sync_playwright
import json
import os

class PlaywrightSessionContext:
    _instance = None
    _state_file = "playwright_session_state.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._playwright = None
            cls._instance._browser = None
            cls._instance._context = None
            cls._instance._page = None
            cls._instance._state = None
        return cls._instance

    def _ensure_browser(self):
        if self._playwright is None:
            self._playwright = sync_playwright().start()
        if self._browser is None:
            self._browser = self._playwright.chromium.launch(headless=False)
        if self._context is None:
            self._context = self._browser.new_context()

    def get_page(self):
        if self._page is None:
            self._ensure_browser()
            self._page = self._context.new_page()
            self._page.goto("https://quickdraw.withgoogle.com/")  # Open the Quick, Draw! homepage on first use
        return self._page

    def close(self):
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
        self._browser = None
        self._context = None
        self._page = None
        self._playwright = None

    def get_state(self):
        if self._state is None:
            if os.path.exists(self._state_file):
                with open(self._state_file, "r", encoding="utf-8") as f:
                    self._state = json.load(f)
            else:
                self._state = {}
        return self._state

    def save_state(self):
        if self._state is not None:
            with open(self._state_file, "w", encoding="utf-8") as f:
                json.dump(self._state, f) 