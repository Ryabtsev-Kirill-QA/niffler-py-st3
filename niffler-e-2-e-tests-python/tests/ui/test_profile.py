import allure
from playwright.sync_api import expect
from marks import Pages


@allure.feature('Профиль пользователя')
@allure.story('UI')
class TestProfile:
    @allure.title('Отображение информации в профиле')
    @Pages.open_profile_page
    def test_profile_info(self, profile_page, envs):
        with allure.step('ОР: Информация о пользователе корректно отображаетсяв профиле'):
            expect(profile_page.profile_page_title).to_contain_text('Profile')
            expect(profile_page.page.get_by_text('Upload new picture')).to_be_visible()
            expect(profile_page.profile_username).to_have_value(envs.niffler_username)

    @allure.title('Добавление имени пользователя в профиль')
    @Pages.open_profile_page
    def test_add_profile_name(self, profile_page):
        name = "test_name"
        profile_page.add_profile_name(name)

        with allure.step('ОР: Добавленное имя отображается в профиле'):
            expect(profile_page.page.get_by_text('Profile successfully updated')).to_be_visible()
            expect(profile_page.profile_name).to_have_value(name)

    @allure.title('Удаление имени пользователя в профиле')
    @Pages.open_profile_page
    def test_delete_profile_name(self, profile_page):
        profile_page.add_profile_name_if_empty()

        profile_page.add_profile_name("")

        with allure.step('ОР: Удаленное имя не отображается в профиле'):
            expect(profile_page.page.get_by_text('Profile successfully updated')).to_be_visible()
            expect(profile_page.profile_name).to_have_text("")
