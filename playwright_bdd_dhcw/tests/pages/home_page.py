import re
from playwright.sync_api import Page, expect
from framework.base.base_page import BasePage

class HomePage(BasePage):

    NAV = "nav"  
    SEARCHBOX_ROLE = "searchbox"
    SEARCH_LABEL = "Search"      
    COOKIE_ACCEPT = "#ccc-notify-accept"
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
        nav = self.page.get_by_role("navigation")
        link = nav.get_by_role("link", name=text, exact=False).first
        expect(link).to_be_visible()
        link.click()

    def click_nav_link(self, name: str, max_scrolls: int = 12, step: int = 1200):

        pat = re.compile(re.escape(name), re.I)
        link = self.page.get_by_role("navigation").get_by_role("link", name=pat).first
        if link.count():
            try:
                link.scroll_into_view_if_needed()
            except Exception:
                pass
            expect(link).to_be_visible()
            link.click()
            return

        for _ in range(max_scrolls):
            link = self.page.get_by_role("link", name=pat).first
            if link.count():
                try:
                    link.scroll_into_view_if_needed()
                except Exception:
                    pass
                expect(link).to_be_visible()
                link.click()
                return

            self.page.mouse.wheel(0, step)
            self.page.wait_for_timeout(200)

        raise AssertionError(f"Link not found: {name}")

    def search(self, text: str):
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

    def should_see_search_results(self, text: str = "search results"):
        pattern = re.compile(re.escape(text), re.I)
        heading = self.page.get_by_role("heading", name=pattern)
        expect(heading).to_be_visible(timeout=10000)

    def assert_results_containing(self, text: str):
        container = self._results_container()
        if container.count():
            expect(container.get_by_text(text, exact=False).first).to_be_visible(timeout=10000)
        else:
            expect(self.page.get_by_text(text, exact=False).first).to_be_visible(timeout=10000)

    def _results_container(self):
        return self.page.locator(
            "#svSearchResults"
        )