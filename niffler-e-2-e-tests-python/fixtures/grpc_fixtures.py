import grpc
import pytest
from grpc import insecure_channel

from grpc_proto.grpc.interceptors.allure import AllureInterceptor
from grpc_proto.grpc.interceptors.logging import LoggingInterceptor
from grpc_proto.internal.pb.niffler_currency_pb2_pbreflect import NifflerCurrencyServiceClient
from settings.settings import Settings

INTERCEPTORS = [
    LoggingInterceptor(),
    AllureInterceptor(),
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
def grpc_client(
        settings: Settings, request: pytest.FixtureRequest
) -> NifflerCurrencyServiceClient:
    host = settings.currency_service_host
    if request.config.getoption("--grpc-mock"):
        host = settings.wiremock_host
    channel = insecure_channel(host)
    intercepted_channel = grpc.intercept_channel(channel, *INTERCEPTORS)
    return NifflerCurrencyServiceClient(intercepted_channel)
