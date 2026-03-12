import allure

from grpc_proto.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from google.protobuf import empty_pb2
from grpc_proto.internal.pb.niffler_currency_pb2 import CurrencyValues as ProtoCurrency


@allure.feature('Конвертер валют')
@allure.story('grpc')
class TestGrpcAll:
    @allure.title('grpc: Получение всех доступных валют')
    def test_get_all_currencies(self, grpc_client: NifflerCurrencyServiceClient) -> None:
        with allure.step("Отправить gRPC-запрос на получение всех валют"):
            response = grpc_client.get_all_currencies(empty_pb2.Empty())
        with allure.step("Число валют в ответе равно 4"):
            assert len(response.allCurrencies) == 4
        with allure.step("Все валюты есть в ответе"):
            currency_values = [c.currency for c in response.allCurrencies]
            assert ProtoCurrency.RUB in currency_values
            assert ProtoCurrency.KZT in currency_values
            assert ProtoCurrency.EUR in currency_values
            assert ProtoCurrency.USD in currency_values

    @allure.title('grpc: Получение всех курсов валют')
    def test_get_all_currencies_rates(self, grpc_client: NifflerCurrencyServiceClient) -> None:
        expected_currency_to_rate = {
            ProtoCurrency.RUB: 0.015,
            ProtoCurrency.KZT: 0.0021,
            ProtoCurrency.EUR: 1.08,
            ProtoCurrency.USD: 1.0
        }
        with allure.step("Отправить gRPC-запрос на получение всех валют"):
            response = grpc_client.get_all_currencies(empty_pb2.Empty())

        with allure.step("Проверить корректность курсов валют в ответе"):
            resp_currencies = {c.currency: c.currencyRate for c in response.allCurrencies}

            assert expected_currency_to_rate[ProtoCurrency.RUB] == resp_currencies[ProtoCurrency.RUB]
            assert expected_currency_to_rate[ProtoCurrency.KZT] == resp_currencies[ProtoCurrency.KZT]
            assert expected_currency_to_rate[ProtoCurrency.EUR] == resp_currencies[ProtoCurrency.EUR]
            assert expected_currency_to_rate[ProtoCurrency.USD] == resp_currencies[ProtoCurrency.USD]
