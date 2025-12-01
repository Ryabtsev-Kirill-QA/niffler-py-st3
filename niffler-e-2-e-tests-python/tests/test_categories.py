from playwright.sync_api import expect
from marks import Pages, TestData


TEST_CATEGORY = "test_category"
TEST_CATEGORY_BD = "test_category_bd"


@TestData.category(TEST_CATEGORY)
@Pages.open_profile_page
def test_edit_category_name_ui(profile_page, category):
    new_name = "new_name"
    profile_page.edit_first_category_name(new_name)
    expect(profile_page.category_name.first).to_have_text(new_name)
    profile_page.edit_first_category_name(category)
    expect(profile_page.category_name.first).to_have_text(category)


@TestData.category(TEST_CATEGORY)
@Pages.open_profile_page
def test_archive_category_ui(profile_page, category):
    profile_page.archive_first_category()

    expect(profile_page.page.get_by_text(category).first).not_to_be_in_viewport()


@TestData.category(TEST_CATEGORY)
@Pages.open_profile_page
def test_unarchive_category_ui(profile_page, category):
    profile_page.archive_first_category()
    profile_page.unarchive_category(category)

    expect(profile_page.page.get_by_text(category).first).to_be_visible()


@TestData.category(TEST_CATEGORY_BD)
def test_add_category_and_check_db(envs, category, spend_db):
    user_categories = spend_db.get_user_categories(envs.niffler_username)
    user_category_names = [category.name for category in user_categories]

    assert len(user_categories) > 0, "Категорий у этого пользовтаеля нет"
    assert category in user_category_names


def test_delete_category_and_check_db(envs, spend_db):
    new_category = spend_db.add_user_category(envs.niffler_username, TEST_CATEGORY_BD)

    search_before_delete = spend_db.get_category_by_id(new_category.id)
    assert search_before_delete.name == TEST_CATEGORY_BD

    spend_db.delete_category(new_category.id)

    search_after_delete = spend_db.get_category_by_name(envs.niffler_username, new_category.name)
    assert search_after_delete is None
