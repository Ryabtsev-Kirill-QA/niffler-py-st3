import allure
from playwright.sync_api import expect


@allure.feature('Выход из системы')
class TestCategory:

    @allure.title('Редактирование названия категории через UI')
    def test_logout(self, setup_auth_state, page_with_auth, spending_page):
        spending_page.navigate_to_spending_page()

        spending_page.logout()

        with allure.step('ОР: Пользователь успешно вышел из системы'):
            expect(spending_page.page.get_by_text("Log in").first).to_be_visible()
