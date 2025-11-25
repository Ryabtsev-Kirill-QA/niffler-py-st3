from faker import Faker
from playwright.sync_api import expect
from marks import TestData

TEST_CATEGORY = "test_category"


@TestData.category(TEST_CATEGORY)
@TestData.spends({
    "amount": 101.1,
    "description": "test_description",
    "category": {
        "name": TEST_CATEGORY
    },
    "spendDate": "2025-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_add_new_spending(envs, spending_page, spend_db, clean_spendings_setup, category, spends):
    spending_page.navigate_to_spending_page()

    added_spend_in_db = spend_db.get_spend_in_db(envs.niffler_username)
    assert added_spend_in_db[0].amount == spends.amount
    assert added_spend_in_db[0].description == spends.description
    assert added_spend_in_db[0].currency == spends.currency

    expect(spending_page.page.get_by_text('History of Spendings')).to_be_visible()
    expect(spending_page.spendings_table).to_contain_text(str(spends.amount))
    expect(spending_page.spendings_table).to_contain_text(TEST_CATEGORY)
    expect(spending_page.spendings_table).to_contain_text(spends.description)


@TestData.category(TEST_CATEGORY)
@TestData.spends({
    "amount": "101.1",
    "description": "test_description",
    "category": {
        "name": TEST_CATEGORY
    },
    "spendDate": "2025-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_update_spending(spending_page, clean_spendings_setup, category, spends):
    faker = Faker()
    new_amount = faker.random_number()
    new_category = "test_new_category"
    new_description = faker.word()

    spending_page.navigate_to_spending_page()

    spending_page.edit_spending_button.last.click()
    spending_page.add_edit_spending(new_amount, new_category, new_description)

    expect(spending_page.page.get_by_text('History of Spendings')).to_be_visible()
    expect(spending_page.spendings_table).not_to_contain_text(str(spends.amount))
    expect(spending_page.spendings_table).not_to_contain_text(category)
    expect(spending_page.spendings_table).not_to_contain_text(spends.description)
    expect(spending_page.spendings_table).to_contain_text(new_category)
    expect(spending_page.spendings_table).to_contain_text(f'{new_amount}')
    expect(spending_page.spendings_table).to_contain_text(new_description)


@TestData.category(TEST_CATEGORY)
@TestData.spends({
    "amount": "101.1",
    "description": "test_description",
    "category": {
        "name": TEST_CATEGORY
    },
    "spendDate": "2025-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_delete_spending(spending_page, clean_spendings_setup, category, spends):
    spending_page.navigate_to_spending_page()

    spending_page.delete_spending()

    expect(spending_page.page.get_by_text("Spendings succesfully deleted")).to_be_visible()
    expect(spending_page.page.get_by_text('History of Spendings')).to_be_visible()
    expect(spending_page.spendings_table).not_to_contain_text(str(spends.amount))
    expect(spending_page.spendings_table).not_to_contain_text(category)
    expect(spending_page.spendings_table).not_to_contain_text(spends.description)


@TestData.category(TEST_CATEGORY)
@TestData.spends({
    "amount": "101.1",
    "description": "test_description",
    "category": {
        "name": TEST_CATEGORY
    },
    "spendDate": "2025-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_delete_all_spendings(spending_page, clean_spendings_setup, category, spends):
    faker = Faker()
    amount = faker.random_number()
    category = "test_category"
    description = faker.word()

    spending_page.navigate_to_spending_page()
    spending_page.click_new_spending()
    spending_page.add_new_spending(amount, category, description)

    spending_page.delete_all_spendings()

    expect(spending_page.page.get_by_text("Spendings succesfully deleted")).to_be_visible()
    expect(spending_page.page.get_by_text('History of Spendings')).to_be_visible()
    expect(spending_page.page.get_by_text('There are no spendings')).to_be_visible()


@TestData.category(TEST_CATEGORY)
def test_total_category_spending_sum(spending_page, category, clean_spendings_setup):
    faker = Faker()
    amount_1 = faker.random_number()
    amount_2 = faker.random_number()
    description = faker.word()

    spending_page.navigate_to_spending_page()
    spending_page.click_new_spending()
    spending_page.add_new_spending(amount_1, category, description)
    spending_page.click_new_spending()
    spending_page.add_new_spending(amount_2, category, description)

    expect(spending_page.category_spending_sum).to_contain_text(f'{amount_1 + amount_2}')


@TestData.category(TEST_CATEGORY)
@TestData.spends({
    "amount": "101.1",
    "description": "test_description",
    "category": {
        "name": TEST_CATEGORY
    },
    "spendDate": "2025-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_valid_spending_search(spending_page, clean_spendings_setup, category, spends):
    spending_page.navigate_to_spending_page()

    spending_page.search_spending(spends.description)

    expect(spending_page.page.get_by_text('History of Spendings')).to_be_visible()
    expect(spending_page.spendings_table).to_contain_text(str(spends.amount))
    expect(spending_page.spendings_table).to_contain_text(category)
    expect(spending_page.spendings_table).to_contain_text(spends.description)


@TestData.category(TEST_CATEGORY)
@TestData.spends({
    "amount": "101.1",
    "description": "test_description",
    "category": {
        "name": TEST_CATEGORY
    },
    "spendDate": "2025-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_invalid_spending_search(spending_page, clean_spendings_setup, category, spends):
    spending_page.navigate_to_spending_page()

    spending_page.search_spending('invalid_search')

    expect(spending_page.page.get_by_text('There are no spendings')).to_be_visible()
    expect(spending_page.page.get_by_text('History of Spendings')).to_be_visible()
    expect(spending_page.spendings_table).not_to_contain_text(str(spends.amount))
    expect(spending_page.spendings_table).not_to_contain_text(category)
    expect(spending_page.spendings_table).not_to_contain_text(spends.description)


@TestData.category(TEST_CATEGORY)
@TestData.spends({
    "amount": "101.1",
    "description": "test_description",
    "category": {
        "name": TEST_CATEGORY
    },
    "spendDate": "2025-08-08T18:39:27.955Z",
    "currency": "RUB"
})
def test_currency_in_amount(spending_page, clean_spendings_setup, category, spends):
    spending_page.navigate_to_spending_page()

    expect(spending_page.spendings_table).to_contain_text("₽")
    expect(spending_page.spendings_table).to_contain_text(str(spends.amount))
