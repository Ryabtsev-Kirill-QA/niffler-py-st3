from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, auth_url):
        super().__init__(page)
        self.auth_url = auth_url

        self.username_input = page.locator("[name=username]")
        self.password_input = page.locator("[name=password]")
        self.submit_button = page.locator("[type='submit']")
        self.error_message = page.locator("[class='form__error-container']")
        self.header = page.locator("[class='header']")
        self.login_text = page.get_by_text("Log in")
        self.app_name = page.locator("[href='/main']")
        self.spending_page_name = page.locator("[href='/spending']")

    def navigate_to_auth_page(self):
        self.go_to(self.auth_url)
        self.wait_for_load()

    def fill_username(self, username: str):
        self.username_input.fill(username)

    def fill_password(self, password: str):
        self.password_input.fill(password)

    def click_submit(self):
        self.submit_button.click()
        self.wait_for_load()

    def login(self, username: str, password: str):
        self.fill_username(username)
        self.fill_password(password)
        self.click_submit()
