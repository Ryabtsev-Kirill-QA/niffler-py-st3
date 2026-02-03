import os
import json
import pytest
import allure
from allure_commons.reporter import AllureReporter
from allure_pytest.listener import AllureListener
from allure_commons.types import AttachmentType
from dotenv import load_dotenv
from pytest import FixtureDef, FixtureRequest
from playwright.sync_api import Browser
from pages.auth_page import LoginPage
from models.config import Envs

pytest_plugins = ["fixtures.auth_fixtures", "fixtures.client_fixtures", "fixtures.pages_fixtures",
                  "fixtures.kafka_fixtures"]


@allure.title('Получаем переменные окружения')
@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    envs_instance = Envs(frontend_url=os.getenv("FRONT_URL"),
                         api_url=os.getenv("API_URL"),
                         auth_url=os.getenv("AUTH_URL"),
                         spend_db_url=os.getenv("SPEND_DB_URL"),
                         userdata_db_url=os.getenv("USER_DB_URL"),
                         kafka_address=os.getenv("KAFKA_ADDRESS"),
                         niffler_username=os.getenv('NIFFLER_USER'),
                         niffler_password=os.getenv('NIFFLER_PASSWORD')
                         )
    allure.attach(envs_instance.model_dump_json(indent=2), name="envs.json", attachment_type=AttachmentType.JSON)
    return envs_instance


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


@allure.title('Страница с предустановленной авторизацией')
@pytest.fixture(scope="function")
def page_with_auth(browser: Browser, setup_auth_state):
    context = browser.new_context(storage_state=str(setup_auth_state))
    page = context.new_page()

    yield page

    context.close()


def allure_logger(config) -> AllureReporter:
    """Получает логгер Аллюра из плагина pytest"""
    listener: AllureListener = config.pluginmanager.get_plugin("allure_listener")
    return listener.allure_logger


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: FixtureDef, request: FixtureRequest):
    """Переименовывает фикстуры в Аллюре"""
    yield
    logger = allure_logger(request.config)
    item = logger.get_last_item()
    scope_letter = fixturedef.scope[0].upper()
    item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_teardown(item):
    """Фильтрует метки в отчете аллюра"""
    yield
    reporter = allure_logger(item.config)
    test = reporter.get_test(None)
    test.labels = list(filter(lambda x: x.name not in ("suite", "subSuite", "parentSuite"), test.labels))
