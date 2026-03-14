import allure
import grpc
import pytest
from grpc_proto.internal.pb.niffler_currency_pb2 import (
    CalculateRequest,
    CurrencyValues,
)
from grpc_proto.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient


@allure.feature('Конвертер валют')
@allure.story('grpc')
class TestGrpcRate:
    @allure.title('grpc: Рассчет конвертации евро в рубли')
    def test_calculate_rate(self, grpc_client: NifflerCurrencyServiceClient) -> None:
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.EUR,
                desiredCurrency=CurrencyValues.RUB,
                amount=100.0,
            )
        )
        assert response.calculatedAmount == 7200, "Expected 7200"

    @allure.title('grpc: Рассчет конвертации евро, не указано в какую валюту')
    def test_calculate_rate__without_desired_currency(self,
                                                      grpc_client: NifflerCurrencyServiceClient,
                                                      ) -> None:
        try:
            response = grpc_client.calculate_rate(
                request=CalculateRequest(
                    spendCurrency=CurrencyValues.EUR,
                    amount=100.0,
                )
            )
        except grpc.RpcError as e:
            assert e.code() == grpc.StatusCode.UNKNOWN
            assert e.details() == "Application error processing RPC"

    @pytest.mark.parametrize(
        "spend, spend_currency, desired_currency, expected_result",
        [
            (100.0, CurrencyValues.USD, CurrencyValues.RUB, 6666.67),
            (100.0, CurrencyValues.RUB, CurrencyValues.USD, 1.5),
            (100.0, CurrencyValues.USD, CurrencyValues.USD, 100.0),
        ],
    )
    @allure.title('grpc: Конвертация валют')
    def test_currency_conversion(self,
                                 grpc_client: NifflerCurrencyServiceClient,
                                 spend: float,
                                 spend_currency: CurrencyValues,
                                 desired_currency: CurrencyValues,
                                 expected_result: float,
                                 ):
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=spend_currency,
                desiredCurrency=desired_currency,
                amount=spend,
            )
        )
        assert response.calculatedAmount == expected_result, f"Expected {expected_result}"

    @allure.title('grpc: Конвертация USD в EUR')
    def test_convert_usd_to_eur(self, grpc_client: NifflerCurrencyServiceClient) -> None:
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.USD,
                desiredCurrency=CurrencyValues.EUR,
                amount=50.0,
            )
        )
        assert response.calculatedAmount == 46.3, "Expected 46.3"

    @allure.title('grpc: Конвертация с нулевой суммой')
    def test_zero_amount(self, grpc_client: NifflerCurrencyServiceClient) -> None:
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.USD,
                desiredCurrency=CurrencyValues.RUB,
                amount=0.0,
            )
        )
        assert response.calculatedAmount == 0.0, "Expected 0.0"

    @allure.title('grpc: Конвертация с отрицательной суммой')
    def test_negative_amount(self, grpc_client: NifflerCurrencyServiceClient) -> None:
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.USD,
                desiredCurrency=CurrencyValues.RUB,
                amount=-100.0,
            )
        )
        assert response.calculatedAmount == -6666.67, "Expected -6666.67"

    @allure.title('grpc: Конвертация с минимальной суммой')
    def test_min_amount(self, grpc_client: NifflerCurrencyServiceClient) -> None:
        response = grpc_client.calculate_rate(
            request=CalculateRequest(
                spendCurrency=CurrencyValues.USD,
                desiredCurrency=CurrencyValues.RUB,
                amount=0.01,
            )
        )
        assert response.calculatedAmount == 0.67, "Expected 0.67"
