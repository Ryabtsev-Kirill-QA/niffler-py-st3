import pytest


@pytest.fixture(params=[])
def category(request, spends_client, spend_db):
    """Добавление категории трат"""
    category_name = request.param
    category = spends_client.add_category(category_name)
    yield category.name
    spend_db.delete_category(category.id)


@pytest.fixture(params=[])
def spends(request, spends_client):
    """Добавление траты"""
    spend = spends_client.add_spends(request.param)
    yield spend
    all_spends = spends_client.get_spends()
    if spend.id in [s.id for s in all_spends]:
        spends_client.remove_spends([spend.id])


@pytest.fixture(scope="function")
def clean_spendings_setup(spends_client):
    """Удаление всех трат до и после теста"""
    all_spendings = spends_client.get_spends()
    spending_ids = [spending.id for spending in all_spendings]
    if spending_ids:
        spends_client.remove_spends(spending_ids)

    yield

    all_spendings = spends_client.get_spends()
    spending_ids = [spending.id for spending in all_spendings]
    if spending_ids:
        spends_client.remove_spends(spending_ids)


@pytest.fixture(scope="function")
def clean_categories(spends_client, spend_db):
    """Удаление всех категорий после теста"""
    yield
    all_categories = spends_client.get_categories()
    categories_ids = [category.id for category in all_categories]
    if categories_ids:
        for categories_id in categories_ids:
            spend_db.delete_category(categories_id)
