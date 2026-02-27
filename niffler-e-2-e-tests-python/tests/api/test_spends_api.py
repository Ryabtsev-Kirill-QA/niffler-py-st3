import allure
import pytest
from models.enums import Category, Currency
from models.spend import SpendEdit
from utils.api_assertions import assertEqual, assertNotIn
from utils.datetime_helper import get_past_date_iso


@allure.feature('Таблица трат')
@allure.story('API')
class TestSpendsApi:
    @allure.title('Создание траты через API')
    @pytest.mark.xdist_group(name="categories_tests")
    def test_add_spend_api(self, spends_client, envs, clean_categories, clean_spendings_setup):
        with allure.step('Отправить запрос на создание траты через API'):
            data = {
                "amount": 101.1,
                "description": "test_description",
                "category": {
                    "name": Category.TEST_CATEGORY
                },
                "spendDate": get_past_date_iso(),
                "currency": Currency.RUB
            }
            new_spend = spends_client.add_spends(data)

        assertEqual(new_spend.amount, data["amount"],
                    "В ответе приходит сумма, которую передавали при создании")
        assertEqual(new_spend.description, data["description"],
                    "В ответе приходит описание, которое передавали при создании")
        assertEqual(new_spend.category.name, data["category"]["name"],
                    "В ответе приходит имя категории, которое передавали при создании")
        assertEqual(str(new_spend.spendDate)[:10], data["spendDate"][:10],
                    "В ответе приходит дата, которую передавали при создании")
        assertEqual(new_spend.currency, data["currency"],
                    "В ответе приходит валюта, которую передавали при создании")

    @allure.title('Удаление траты через API')
    @pytest.mark.xdist_group(name="categories_tests")
    def test_delete_spend_api(self, spends_client, spend_db, envs, clean_categories):
        with allure.step('Отправить запрос на создание траты через API'):
            data = {
                "amount": 101.1,
                "description": "test_description",
                "category": {
                    "name": Category.TEST_CATEGORY
                },
                "spendDate": get_past_date_iso(),
                "currency": Currency.RUB
            }
            new_spend = spends_client.add_spends(data)
        with allure.step('Отправить запрос на удаление траты через API'):
            spends_client.remove_spends(new_spend.id)
        with allure.step('Отправить запрос на получение трат через API'):
            all_spends = spends_client.get_spends()

            assertNotIn(new_spend.id, [s.id for s in all_spends], "Созданная трата отсутствует")

    @allure.title('Редактирование траты через API')
    @pytest.mark.xdist_group(name="categories_tests")
    def test_edit_spend_api(self, spends_client, envs, clean_categories, clean_spendings_setup):
        with allure.step('Отправить запрос на создание траты через API'):
            data = {
                "amount": 101.1,
                "description": "test_description",
                "category": {
                    "name": Category.TEST_CATEGORY
                },
                "spendDate": get_past_date_iso(),
                "currency": Currency.RUB
            }
            new_spend = spends_client.add_spends(data)

        with allure.step('Отправить запрос на редактирование траты через API'):
            new_amount = 111
            new_description = "Отпуск"
            new_currency = Currency.USD
            edit_data = SpendEdit(id=new_spend.id,
                                  spendDate=get_past_date_iso(),
                                  amount=new_amount,
                                  category={
                                      "name": Category.TEST_CATEGORY
                                  },
                                  description=new_description,
                                  currency=new_currency)
            edited_spend = spends_client.edit_spend(edit_data)

        assertEqual(edited_spend.amount, new_amount,
                    "В ответе приходит новая сумма для траты")
        assertEqual(edited_spend.description, new_description,
                    "В ответе приходит новое описание")
        assertEqual(edited_spend.currency, new_currency,
                    "В ответе приходит новая валюта")

    @allure.title('Создание траты со всеми поддерживаемыми валютами через API')
    @pytest.mark.parametrize("currency", [
        Currency.RUB,
        Currency.USD,
        Currency.EUR,
        Currency.KZT
    ])
    @pytest.mark.xdist_group(name="categories_tests")
    def test_add_spend_all_currencies_api(self, spends_client, envs, clean_categories, clean_spendings_setup, currency):
        test_data = {
            Currency.RUB: {"amount": 1000.50, "description": "Трата в рублях"},
            Currency.USD: {"amount": 100.75, "description": "Трата в долларах"},
            Currency.EUR: {"amount": 90.25, "description": "Трата в евро"},
            Currency.KZT: {"amount": 50000.00, "description": "Трата в тенге"}
        }

        amount = test_data[currency]["amount"]
        description = test_data[currency]["description"]
        currency_str = str(currency)

        with allure.step(f'Создать трату в валюте {currency_str}'):
            data = {
                "amount": amount,
                "description": description,
                "category": {
                    "name": Category.TEST_CATEGORY
                },
                "spendDate": get_past_date_iso(),
                "currency": currency_str
            }
            new_spend = spends_client.add_spends(data)

        assertEqual(new_spend.amount, data["amount"],
                    "В ответе приходит сумма, которую передавали при создании")
        assertEqual(new_spend.description, data["description"],
                    "В ответе приходит описание, которое передавали при создании")
        assertEqual(new_spend.category.name, data["category"]["name"],
                    "В ответе приходит имя категории, которое передавали при создании")
        assertEqual(str(new_spend.spendDate)[:10], data["spendDate"][:10],
                    "В ответе приходит дата, которую передавали при создании")
        assertEqual(new_spend.currency, data["currency"],
                    "В ответе приходит валюта, которую передавали при создании")
