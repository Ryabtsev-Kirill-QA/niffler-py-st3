from playwright.sync_api import expect
from marks import Pages


@Pages.open_profile_page
def test_profile_info(profile_page, user_creds):
    expect(profile_page.profile_page_title).to_contain_text('Profile')
    expect(profile_page.page.get_by_text('Upload new picture')).to_be_visible()
    expect(profile_page.profile_username).to_have_value(user_creds["username"])


@Pages.open_profile_page
def test_add_profile_name(profile_page):
    name = "test_name"
    profile_page.add_profile_name(name)

    expect(profile_page.page.get_by_text('Profile successfully updated')).to_be_visible()
    expect(profile_page.profile_name).to_have_value(name)


@Pages.open_profile_page
def test_delete_profile_name(profile_page):
    profile_page.add_profile_name_if_empty()

    profile_page.add_profile_name("")

    expect(profile_page.page.get_by_text('Profile successfully updated')).to_be_visible()
    expect(profile_page.profile_name).to_have_text("")


@Pages.open_profile_page
def test_edit_category_name(profile_page):
    profile_page.add_new_category_if_empty()

    old_name = profile_page.category_name.first.text_content()
    new_name = "new_name"
    profile_page.edit_first_category_name(new_name)
    expect(profile_page.category_name.first).to_have_text(new_name)
    profile_page.edit_first_category_name(old_name)
    expect(profile_page.category_name.first).to_have_text(old_name)


@Pages.open_profile_page
def test_archive_category(profile_page):
    profile_page.add_new_category_if_empty()

    category_name = profile_page.category_name.first.text_content()
    profile_page.archive_first_category()

    expect(profile_page.page.get_by_text(category_name).first).not_to_be_in_viewport()


@Pages.open_profile_page
def test_unarchive_category(profile_page):
    profile_page.add_new_category_if_empty()

    category_name = profile_page.category_name.first.text_content()
    profile_page.archive_first_category()
    profile_page.unarchive_category(category_name)

    expect(profile_page.page.get_by_text(category_name).first).to_be_visible()
