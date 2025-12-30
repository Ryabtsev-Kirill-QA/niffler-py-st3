import allure
from playwright.sync_api import expect
from marks import Pages


@allure.feature('Регистрация')
@allure.story('UI')
class TestRegistration:
    @allure.title('Регистрация нового пользователя в системе')
    @Pages.open_login_page
    def test_sign_up(self, registration_page):
        registration_page.go_to_registration_form()
        registration_page.register_new_user()

        with allure.step('ОР: Отображается страница авторизации'):
            expect(registration_page.sign_in_form).to_be_visible()

    @allure.title('Регистрация нового пользователя с пустыми данными')
    @Pages.open_login_page
    def test_sign_up_empty_fields(self, registration_page):
        registration_page.go_to_registration_form()
        registration_page.click_submit()

        with allure.step('ОР: Продолжает отображаться страница регистрации'):
            expect(registration_page.sign_in_form).not_to_be_visible()
            expect(registration_page.username_input).to_be_visible()
            expect(registration_page.password_input).to_be_visible()

    @allure.title('Регистрация нового пользователя, пароли не совпадают')
    @Pages.open_login_page
    def test_sign_up_passwords_dont_match(self, registration_page):
        username = registration_page.faker.user_name()
        password1 = registration_page.faker.password()
        password2 = registration_page.faker.password()

        registration_page.go_to_registration_form()
        registration_page.register(username, password1, password2)

        with allure.step('ОР: Продолжает отображаться страница регистрации. Сообщение, что пароли не совпадают'):
            expect(registration_page.sign_in_form).not_to_be_visible()
            expect(registration_page.error_message).to_contain_text("Passwords should be equal")
