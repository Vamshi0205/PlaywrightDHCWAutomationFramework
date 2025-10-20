# tests/pages/home_page.py
from playwright.sync_api import Page, expect
from framework.base.base_page import BasePage

class HomePage(BasePage):
    # --- Locators (simple & stable) ---
    NAV = "nav"  # top navigation landmark
    SEARCHBOX_ROLE = "searchbox"
    SEARCH_LABEL = "Search"       # adjust if the visible label differs
    COOKIE_ACCEPT = "#ccc-notify-accept"   # update to your site if needed
    COOKIE_BANNER = "#ccc-notify"

    # --- Actions ---
    def open(self, base_url: str):
        self.goto(base_url)
        self.page.wait_for_load_state("domcontentloaded")
        self.accept_cookies()

    def accept_cookies(self):
        banner = self.page.locator(self.COOKIE_BANNER)
        if banner.count():
            self.page.locator(self.COOKIE_ACCEPT).first.click(timeout=2000)

    def click_nav(self, text: str):
        # Prefer accessible roles inside the nav landmark
        nav = self.page.get_by_role("navigation")
        link = nav.get_by_role("link", name=text, exact=False).first
        expect(link).to_be_visible()
        link.click()

    def search(self, text: str):
        # Try ARIA searchbox first; fall back to labeled textbox
        box = self.page.get_by_role(self.SEARCHBOX_ROLE)
        if box.count() == 0:
            box = self.page.get_by_role("textbox", name=self.SEARCH_LABEL)
        expect(box.first).to_be_visible()
        box.first.fill(text)
        box.first.press("Enter")
        self.page.wait_for_load_state("networkidle")

    # --- Assertions ---
    def should_see_nav_link(self, text: str):
        link = self.page.get_by_role("navigation").get_by_role("link", name=text, exact=False).first
        expect(link).to_be_visible()

    def should_have_title(self, expected: str):
        expect(self.page).to_have_title(expected)

    def should_see_search_results(self):
        # Simple, tolerant heading check
        heading = self.page.get_by_role("heading", name=lambda n: n and "search" in n.lower())
        expect(heading).to_be_visible()

    def url_should_contain(self, snippet: str):
        expect(self.page).to_have_url(lambda u: snippet.lower() in u.lower())
