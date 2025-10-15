from playwright.sync_api import Page, expect

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
