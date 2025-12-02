import allure
from playwright.sync_api import expect
from marks import Pages


@allure.feature('Авторизация')
class TestAuth:

    @allure.title('Авторизация с валидными данными')
    @Pages.open_login_page
    def test_auth(self, login_page, envs):
        login_page.login(envs.niffler_username, envs.niffler_password)

        with allure.step('ОР: Пользователь успешно авторизован в системе'):
            expect(login_page.login_text).not_to_be_visible()
            expect(login_page.app_name).to_contain_text("Niffler")
            expect(login_page.spending_page_name).to_be_visible()

    @allure.title('Авторизация с невалидными данными')
    @Pages.open_login_page
    def test_invalid_auth(self, login_page):
        login_page.login("invalid_user", "invalid_password")

        with allure.step('ОР: Пользователь не авторизован в системе, отображается сообщение об ошибке'):
            error_text = login_page.error_message.text_content()
            assert "Неверные учетные данные пользователя" in error_text or "Bad credentials" in error_text
            expect(login_page.header).to_contain_text("Log in")
            expect(login_page.spending_page_name).not_to_be_visible()
