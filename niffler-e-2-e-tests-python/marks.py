import pytest


class Pages:
    open_login_page = pytest.mark.usefixtures("open_login_page")
    open_profile_page = pytest.mark.usefixtures("setup_auth_state", "page_with_auth", "open_profile_page")


class TestData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    spends = lambda x: pytest.mark.parametrize("spends", [x], indirect=True, ids=lambda param: param["description"])
