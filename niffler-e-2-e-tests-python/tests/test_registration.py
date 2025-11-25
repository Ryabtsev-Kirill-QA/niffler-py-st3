from playwright.sync_api import expect


def test_sign_up(registration_page):
    registration_page.navigate_to_auth_page()
    registration_page.go_to_registration_form()
    registration_page.register_new_user()

    expect(registration_page.sign_in_form).to_be_visible()


def test_sign_up_empty_fields(registration_page):
    registration_page.navigate_to_auth_page()
    registration_page.go_to_registration_form()
    registration_page.click_submit()

    expect(registration_page.sign_in_form).not_to_be_visible()
    expect(registration_page.username_input).to_be_visible()
    expect(registration_page.password_input).to_be_visible()


def test_sign_up_passwords_dont_match(registration_page):
    username = registration_page.faker.user_name()
    password1 = registration_page.faker.password()
    password2 = registration_page.faker.password()

    registration_page.navigate_to_auth_page()
    registration_page.go_to_registration_form()
    registration_page.register(username, password1, password2)

    expect(registration_page.sign_in_form).not_to_be_visible()
    expect(registration_page.error_message).to_contain_text("Passwords should be equal")
