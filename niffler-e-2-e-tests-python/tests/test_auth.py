from playwright.sync_api import expect
from marks import Pages


@Pages.open_login_page
def test_auth(login_page, user_creds):
    login_page.login(user_creds["username"], user_creds["password"])

    expect(login_page.login_text).not_to_be_visible()
    expect(login_page.app_name).to_contain_text("Niffler")
    expect(login_page.spending_page_name).to_be_visible()


@Pages.open_login_page
def test_invalid_auth(login_page):
    login_page.login("invalid_user", "invalid_password")

    error_text = login_page.error_message.text_content()
    assert "Неверные учетные данные пользователя" in error_text or "Bad credentials" in error_text
    expect(login_page.header).to_contain_text("Log in")
    expect(login_page.spending_page_name).not_to_be_visible()
