import os
import json
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page
from playwright.sync_api import Browser

from databases.spend_db import SpendDb
from models.config import Envs
from models.spend import CategoryAdd
from pages.auth_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.spending_page import SpendingPage
from pages.profile_page import ProfilePage
from clients.spends_client import SpendsHttpClient


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(frontend_url=os.getenv("FRONT_URL"),
                api_url=os.getenv("API_URL"),
                auth_url=os.getenv("AUTH_URL"),
                spend_db_url=os.getenv("SPEND_DB_URL"),
                niffler_username=os.getenv('NIFFLER_USER'),
                niffler_password=os.getenv('NIFFLER_PASSWORD')
                )


@pytest.fixture(scope="session")
def spends_client(envs, get_token_from_user_state, playwright) -> SpendsHttpClient:
    return SpendsHttpClient(envs.api_url, get_token_from_user_state, playwright)


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture()
def login_page(page: Page) -> LoginPage:
    login_page = LoginPage(page)
    return login_page


@pytest.fixture()
def open_login_page(login_page, envs):
    login_page.go_to(envs.auth_url)
    login_page.wait_for_load()


@pytest.fixture(scope="function")
def registration_page(page: Page, envs) -> RegistrationPage:
    registration_page = RegistrationPage(page, envs.auth_url)
    return registration_page


@pytest.fixture(scope="function")
def spending_page(page_with_auth: Page, envs) -> SpendingPage:
    spending_page = SpendingPage(page_with_auth, envs.frontend_url)
    return spending_page


@pytest.fixture(scope="function")
def profile_page(page_with_auth: Page) -> ProfilePage:
    profile_page = ProfilePage(page_with_auth)
    return profile_page


@pytest.fixture()
def open_profile_page(profile_page, envs):
    profile_page.go_to(envs.frontend_url + '/profile')
    profile_page.wait_for_load()


@pytest.fixture(params=[])
def category(request, spends_client, spend_db):
    category_name = request.param
    category = spends_client.add_category(CategoryAdd(name=category_name))
    yield category.name
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(request, spends_client):
    spend = spends_client.add_spends(request.param)
    yield spend
    all_spends = spends_client.get_all_spendings()
    if spend.id in [s.id for s in all_spends]:
        spends_client.delete_spending([spend.id])


@pytest.fixture(scope="session")
def setup_auth_state(browser: Browser, envs, tmp_path_factory):
    """Автоматически создает файл с состоянием авторизации перед всеми тестами"""
    temp_dir = tmp_path_factory.mktemp("auth_data")
    state_path = temp_dir / "niffler_user.json"

    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.go_to(envs.auth_url)
    login_page.login(envs.niffler_username, envs.niffler_password)
    login_page.spending_page_name.wait_for(state='visible', timeout=10000)

    context.storage_state(path=str(state_path))
    context.close()

    yield state_path


@pytest.fixture(scope="function")
def page_with_auth(browser: Browser, setup_auth_state):
    """Страница с предустановленной авторизацией"""
    context = browser.new_context(storage_state=str(setup_auth_state))
    page = context.new_page()

    yield page

    context.close()


@pytest.fixture(scope="session")
def get_token_from_user_state(setup_auth_state):
    with open(setup_auth_state) as json_file:
        data = json.load(json_file)
        api_token = data['origins'][0]['localStorage'][3]['value']
    return api_token


@pytest.fixture(scope="function")
def clean_spendings_setup(spends_client):
    spends_client.delete_all_spendings()

    yield

    spends_client.delete_all_spendings()
