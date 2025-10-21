from playwright.sync_api import Locator, Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def click(self, locator):
        self.page.locator(locator).click()

    def fill(self, locator, text: str):
        self.page.locator(locator).fill(text)

    def should_see(self, locator):
        expect(self.page.locator(locator)).to_be_visible()

    def click_visible(self, target: str | Locator, timeout: int = 10_000):
        loc: Locator = target if isinstance(target, Locator) else self.page.locator(str(target)).first
        try:
            loc.scroll_into_view_if_needed(timeout=timeout)
        except Exception:
            pass
        expect(loc).to_be_visible(timeout=timeout)
        loc.click()

    def ensure_visible(self, target: str | Locator, timeout: int = 10_000) -> Locator:
        loc: Locator = target if isinstance(target, Locator) else self.page.locator(str(target)).first
        try:
            loc.scroll_into_view_if_needed(timeout=timeout)
        except Exception:
            pass
        expect(loc).to_be_visible(timeout=timeout)
        return loc
