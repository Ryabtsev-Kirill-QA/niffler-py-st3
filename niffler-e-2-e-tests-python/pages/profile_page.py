import allure
from playwright.sync_api import Page
from pages.base_page import BasePage


class ProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.profile_page_title = page.locator("[class*='MuiTypography-h5 css-w1t7b3']")
        self.profile_username = page.locator("[id='username']")
        self.profile_name = page.locator("[id='name']")
        self.save_changes_button = page.locator("[type='submit']")
        self.add_new_category_input = page.locator("[id='category']")
        self.edit_category_name = page.locator("[aria-label='Edit category']")
        self.category_name = page.locator("[class*='css-14vsv3w']")
        self.edit_category_input = page.locator("[placeholder='Edit category']")
        self.archive_category = page.locator("[aria-label='Archive category']")
        self.unarchive_category_button = page.locator("[data-testid='UnarchiveOutlinedIcon']")
        self.show_archived = page.locator("[type='checkbox']")

    def add_profile_name(self, name: str):
        with allure.step(f'Добавить имя {name} пользователя в профиле'):
            self.profile_name.fill(name)
            self.save_changes_button.click()

    def edit_first_category_name(self, name: str):
        with allure.step('Отредактировать имя первой категории в списке'):
            self.edit_category_name.first.click()
            self.edit_category_input.fill(name)
            self.page.keyboard.press("Enter")

    def add_new_category(self, category_name: str):
        with allure.step('Добавить новую категорию'):
            self.add_new_category_input.fill(category_name)
            self.page.keyboard.press("Enter")

    def archive_first_category(self):
        with allure.step('Заархивировать первую категорию в списке'):
            self.archive_category.first.click()
            self.page.get_by_text("Archive").last.click()

    def unarchive_category(self, name):
        with allure.step('Разархивировать  категорию'):
            self.show_archived.click()
            self.page.locator(
                f"//div[contains(@class, 'MuiChip-root')]//span[text()='{name}']/../following-sibling::span//button").click()
            self.page.get_by_text("Unarchive").last.click()

    def add_profile_name_if_empty(self):
        with allure.step('Если имя в профиле пустое, то добавить его'):
            name = "test_name"
            if self.profile_name.text_content() != name:
                self.add_profile_name(name)
