from playwright.sync_api import Page
from pages.base_page import BasePage
from faker import Faker


class RegistrationPage(BasePage):
    def __init__(self, page: Page, auth_url):
        super().__init__(page)
        self.faker = Faker()
        self.auth_url = auth_url

        self.register_link = page.locator("[class='form__register']")
        self.username_input = page.locator("[id='username']")
        self.password_input = page.locator("[id='password']")
        self.password_confirm_input = page.locator("[id='passwordSubmit']")
        self.submit_button = page.locator("[type='submit']")
        self.sign_in_form = page.locator("[class='form_sign-in']")
        self.error_message = page.locator("[class='form__error']")

    def navigate_to_auth_page(self):
        self.go_to(self.auth_url)
        self.wait_for_load()

    def click_register_link(self):
        self.register_link.click()

    def go_to_registration_form(self):
        self.click_register_link()
        self.wait_for_load()

    def fill_username(self, username: str):
        self.username_input.fill(username)

    def fill_password(self, password: str):
        self.password_input.fill(password)

    def fill_password_confirmation(self, password: str):
        self.password_confirm_input.fill(password)

    def click_submit(self):
        self.submit_button.click()
        self.wait_for_load()

    def register(self, username: str, password: str, confirm_password: str = None):
        self.fill_username(username)
        self.fill_password(password)
        self.fill_password_confirmation(confirm_password or password)
        self.click_submit()

    def register_new_user(self):
        username = self.faker.user_name()
        password = self.faker.password()
        self.register(username, password)
        return username, password
