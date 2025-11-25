from playwright.sync_api import expect


def test_logout(setup_auth_state, page_with_auth, spending_page):
    spending_page.navigate_to_spending_page()

    spending_page.logout()

    expect(spending_page.page.get_by_text("Log in").first).to_be_visible()
