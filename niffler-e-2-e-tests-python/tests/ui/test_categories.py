import allure
from playwright.sync_api import expect
from marks import Pages, TestData
from models.enums import Category


@allure.feature('Категории')
@allure.story('UI')
class TestCategory:
    @allure.title('Редактирование названия категории через UI')
    @TestData.category(Category.TEST_CATEGORY)
    @Pages.open_profile_page
    def test_edit_category_name_ui(self, profile_page, category):
        new_name = "new_name"
        profile_page.edit_first_category_name(new_name)
        with allure.step('ОР: Отображается новое имя категории'):
            expect(profile_page.category_name.first).to_have_text(new_name)
        profile_page.edit_first_category_name(category)
        with allure.step('ОР: Отображается первоначальное имя категории'):
            expect(profile_page.category_name.first).to_have_text(category)

    @allure.title('Архивация категории через UI')
    @TestData.category(Category.TEST_CATEGORY)
    @Pages.open_profile_page
    def test_archive_category_ui(self, profile_page, category):
        profile_page.archive_first_category()

        with allure.step('ОР: Заархивированная категория не отображается на экране'):
            expect(profile_page.page.get_by_text(category).first).not_to_be_in_viewport()

    @allure.title('Разархивация категории через UI')
    @TestData.category(Category.TEST_CATEGORY)
    @Pages.open_profile_page
    def test_unarchive_category_ui(self, profile_page, category):
        profile_page.archive_first_category()
        profile_page.unarchive_category(category)

        with allure.step('ОР: Разархивированная категория отображается на экране'):
            expect(profile_page.page.get_by_text(category).first).to_be_visible()

    @allure.title('Добавление категории через БД')
    @allure.story('DB')
    @TestData.category(Category.TEST_CATEGORY)
    def test_add_category_and_check_db(self, envs, category, spend_db):
        user_categories = spend_db.get_user_categories(envs.niffler_username)
        user_category_names = [category.name for category in user_categories]

        with allure.step('ОР: В БД добавлена запись с новой категорией'):
            assert len(user_categories) > 0, "Категорий у этого пользовтаеля нет"
            assert category in user_category_names

    @allure.title('Удаление категории через БД')
    @allure.story('DB')
    def test_delete_category_and_check_db(self, envs, spend_db):
        new_category = spend_db.add_user_category(envs.niffler_username, Category.TEST_CATEGORY_BD)

        search_before_delete = spend_db.get_category_by_id(new_category.id)
        assert search_before_delete.name == Category.TEST_CATEGORY_BD

        spend_db.delete_category(new_category.id)

        search_after_delete = spend_db.get_category_by_name(envs.niffler_username, new_category.name)
        with allure.step('ОР: В БД удалена запись с новой категорией'):
            assert search_after_delete is None
