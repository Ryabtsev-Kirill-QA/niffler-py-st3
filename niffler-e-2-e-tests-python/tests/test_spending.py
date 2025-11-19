from faker import Faker
from playwright.sync_api import expect


def test_add_new_spending(spending_page, clean_spendings_setup):
    faker = Faker()
    amount = faker.random_number()
    category = "test_category"
    description = faker.word()

    spending_page.navigate_to_spending_page()
    spending_page.click_new_spending()
    spending_page.add_new_spending(amount, category, description)

    expect(spending_page.page.get_by_text('History of Spendings')).to_be_visible()
    expect(spending_page.spendings_table).to_contain_text(str(amount))
    expect(spending_page.spendings_table).to_contain_text(category)
    expect(spending_page.spendings_table).to_contain_text(description)


def test_update_spending(spending_page, clean_spendings_setup):
    faker = Faker()
    old_amount = faker.random_number()
    old_category = "test_category"
    old_description = faker.word()
    new_amount = faker.random_number()
    new_category = "test_new_category"
    new_description = faker.word()

    spending_page.navigate_to_spending_page()
    spending_page.click_new_spending()
    spending_page.add_new_spending(old_amount, old_category, old_description)

    spending_page.edit_spending_button.last.click()

    spending_page.add_new_spending(new_amount, new_category, new_description)

    expect(spending_page.page.get_by_text('History of Spendings')).to_be_visible()
    expect(spending_page.spendings_table).not_to_contain_text(str(old_amount))
    expect(spending_page.spendings_table).not_to_contain_text(old_description)
    expect(spending_page.spendings_table).not_to_contain_text(old_category)
    expect(spending_page.spendings_table).to_contain_text(new_category)
    expect(spending_page.spendings_table).to_contain_text(f'{new_amount}')
    expect(spending_page.spendings_table).to_contain_text(new_description)


def test_delete_spending(spending_page, clean_spendings_setup):
    faker = Faker()
    amount = faker.random_number()
    category = "test_category"
    description = faker.word()

    spending_page.navigate_to_spending_page()
    spending_page.click_new_spending()
    spending_page.add_new_spending(amount, category, description)

    spending_page.delete_spending()

    expect(spending_page.page.get_by_text("Spendings succesfully deleted")).to_be_visible()
    expect(spending_page.page.get_by_text('History of Spendings')).to_be_visible()
    expect(spending_page.spendings_table).not_to_contain_text(str(amount))
    expect(spending_page.spendings_table).not_to_contain_text(description)
    expect(spending_page.spendings_table).not_to_contain_text(category)


def test_delete_all_spendings(spending_page, clean_spendings_setup):
    faker = Faker()
    amount = faker.random_number()
    category = "test_category"
    description = faker.word()

    spending_page.navigate_to_spending_page()
    spending_page.click_new_spending()
    spending_page.add_new_spending(amount, category, description)
    spending_page.click_new_spending()
    spending_page.add_new_spending(amount, category, description)

    spending_page.delete_all_spendings()

    expect(spending_page.page.get_by_text("Spendings succesfully deleted")).to_be_visible()
    expect(spending_page.page.get_by_text('History of Spendings')).to_be_visible()
    expect(spending_page.page.get_by_text('History of Spendings')).to_be_visible()
    expect(spending_page.page.get_by_text('There are no spendings')).to_be_visible()


def test_total_category_spending_sum(spending_page, clean_spendings_setup):
    faker = Faker()
    amount_1 = faker.random_number()
    amount_2 = faker.random_number()
    category = "test_category"
    description = faker.word()

    spending_page.navigate_to_spending_page()
    spending_page.click_new_spending()
    spending_page.add_new_spending(amount_1, category, description)
    spending_page.click_new_spending()
    spending_page.add_new_spending(amount_2, category, description)

    expect(spending_page.category_spending_sum).to_contain_text(f'{amount_1 + amount_2}')

