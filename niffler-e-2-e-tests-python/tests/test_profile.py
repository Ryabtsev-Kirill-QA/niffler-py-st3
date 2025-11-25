from playwright.sync_api import expect
from marks import Pages


TEST_CATEGORY = "test_category"


@Pages.open_profile_page
def test_profile_info(profile_page, envs):
    expect(profile_page.profile_page_title).to_contain_text('Profile')
    expect(profile_page.page.get_by_text('Upload new picture')).to_be_visible()
    expect(profile_page.profile_username).to_have_value(envs.niffler_username)


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
