import os
import json
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page
from playwright.sync_api import Browser
from pages.auth_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.spending_page import SpendingPage
from api.api_methods import ApiMethods

load_dotenv()


@pytest.fixture(scope="session")
def user_creds():
    return {
        'username': os.getenv('NIFFLER_USER'),
        'password': os.getenv('NIFFLER_PASSWORD'),
    }


@pytest.fixture(scope="function")
def login_page(page: Page) -> LoginPage:
    auth_url = os.getenv('AUTH_URL')
    login_page = LoginPage(page, auth_url)
    return login_page


@pytest.fixture(scope="function")
def registration_page(page: Page) -> RegistrationPage:
    auth_url = os.getenv('AUTH_URL')
    registration_page = RegistrationPage(page, auth_url)
    return registration_page


@pytest.fixture(scope="function")
def spending_page(page_with_auth: Page) -> SpendingPage:
    front_url = os.getenv('FRONT_URL')
    spending_page = SpendingPage(page_with_auth, front_url)
    return spending_page


@pytest.fixture(scope="session", autouse=True)
def setup_auth_state(browser: Browser, user_creds):
    """Автоматически создает файл с состоянием авторизации перед всеми тестами"""
    context = browser.new_context()
    page = context.new_page()

    auth_url = os.getenv('AUTH_URL')
    login_page = LoginPage(page, auth_url)
    login_page.navigate_to_auth_page()
    login_page.login(user_creds["username"], user_creds["password"])
    login_page.spending_page_name.wait_for(state='visible', timeout=10000)

    context.storage_state(path="./niffler_user.json")
    context.close()

    yield

    os.remove("./niffler_user.json")


@pytest.fixture(scope="function")
def page_with_auth(browser: Browser):
    """Страница с предустановленной авторизацией"""
    context = browser.new_context(storage_state="./niffler_user.json")
    page = context.new_page()

    yield page

    context.close()


@pytest.fixture(scope="function")
def get_token_from_user_state():
    with open('niffler_user.json') as json_file:
        data = json.load(json_file)
        api_token = data['origins'][0]['localStorage'][3]['value']
    return api_token


@pytest.fixture(scope="function")
def clean_spendings_setup(playwright, get_token_from_user_state):
    api_methods = ApiMethods()

    api_methods.delete_all_spendings(playwright, get_token_from_user_state)

    yield

    api_methods.delete_all_spendings(playwright, get_token_from_user_state)
