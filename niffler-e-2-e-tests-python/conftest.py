import os
import json
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page
from playwright.sync_api import Browser
from pages.auth_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.spending_page import SpendingPage
from pages.profile_page import ProfilePage
from clients.spends_client import SpendsHttpClient


@pytest.fixture(scope="session")
def envs():
    load_dotenv()


@pytest.fixture(scope="session")
def frontend_url(envs):
    return os.getenv("FRONT_URL")


@pytest.fixture(scope="session")
def api_url(envs):
    return os.getenv("API_URL")


@pytest.fixture(scope="session")
def auth_url(envs):
    return os.getenv("AUTH_URL")


@pytest.fixture(scope="session")
def user_creds(envs):
    return {
        'username': os.getenv('NIFFLER_USER'),
        'password': os.getenv('NIFFLER_PASSWORD'),
    }


@pytest.fixture(scope="session")
def spends_client(api_url, get_token_from_user_state, playwright) -> SpendsHttpClient:
    return SpendsHttpClient(api_url, get_token_from_user_state, playwright)


@pytest.fixture()
def login_page(page: Page) -> LoginPage:
    login_page = LoginPage(page)
    return login_page


@pytest.fixture()
def open_login_page(login_page, auth_url):
    login_page.go_to(auth_url)
    login_page.wait_for_load()


@pytest.fixture(scope="function")
def registration_page(page: Page, auth_url) -> RegistrationPage:
    registration_page = RegistrationPage(page, auth_url)
    return registration_page


@pytest.fixture(scope="function")
def spending_page(page_with_auth: Page, frontend_url) -> SpendingPage:
    spending_page = SpendingPage(page_with_auth, frontend_url)
    return spending_page


@pytest.fixture(scope="function")
def profile_page(page_with_auth: Page) -> ProfilePage:
    profile_page = ProfilePage(page_with_auth)
    return profile_page


@pytest.fixture()
def open_profile_page(profile_page, frontend_url):
    profile_page.go_to(frontend_url + '/profile')
    profile_page.wait_for_load()


@pytest.fixture(params=[])
def category(request, spends_client):
    category_name = request.param
    current_categories = spends_client.get_categories()
    category_names = [category["name"] for category in current_categories]
    if category_name not in category_names:
        spends_client.add_category(category_name)
    return category_name


@pytest.fixture(params=[])
def spends(request, spends_client):
    spend = spends_client.add_spends(request.param)
    yield spend
    all_spends = spends_client.get_all_spendings()
    all_spends_data = all_spends.json()
    if spend["id"] in [s["id"] for s in all_spends_data.get('content', [])]:
        spends_client.delete_all_spendings()


@pytest.fixture(scope="session")
def setup_auth_state(browser: Browser, auth_url, user_creds):
    """Автоматически создает файл с состоянием авторизации перед всеми тестами"""
    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.go_to(auth_url)
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


@pytest.fixture(scope="session")
def get_token_from_user_state(setup_auth_state):
    with open('niffler_user.json') as json_file:
        data = json.load(json_file)
        api_token = data['origins'][0]['localStorage'][3]['value']
    return api_token


@pytest.fixture(scope="function")
def clean_spendings_setup(spends_client):
    spends_client.delete_all_spendings()

    yield

    spends_client.delete_all_spendings()
