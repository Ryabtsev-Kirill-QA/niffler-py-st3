from playwright.sync_api import APIResponse
from models.spend import Category, Spend, SpendAdd, CategoryAdd


class SpendsHttpClient:
    base_url: str

    def __init__(self, base_url: str, token: str, playwright):
        self.base_url = base_url
        self.request_context = playwright.request.new_context(
            base_url=base_url,
            extra_http_headers={
                'Accept': 'application/json',
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
        )

    def get_categories(self) -> list[CategoryAdd]:
        response = self.request_context.get("/api/categories/all")
        self.raise_for_status(response)
        return [CategoryAdd.model_validate(item) for item in response.json()]

    def add_category(self, category: CategoryAdd) -> Category:
        category = CategoryAdd.model_validate(category)
        response = self.request_context.post("/api/categories/add", data=category.model_dump())
        self.raise_for_status(response)
        return Category.model_validate(response.json())

    def add_spends(self, spend: dict) -> Spend:
        spend_data = SpendAdd.model_validate(spend)
        response = self.request_context.post("/api/spends/add", data=spend_data.model_dump())
        self.raise_for_status(response)
        return Spend.model_validate(response.json())

    def get_all_spendings(self) -> list[Spend]:
        response = self.request_context.get("/api/v2/spends/all")
        self.raise_for_status(response)
        return [Spend.model_validate(item) for item in response.json()["content"]]

    def delete_spending(self, ids: list[str]):
        ids_param = ",".join(ids)
        response = self.request_context.delete("/api/spends/remove", params={"ids": ids_param})
        self.raise_for_status(response)

    def delete_all_spendings(self):
        all_spendings = self.get_all_spendings()
        spending_ids = [spending.id for spending in all_spendings]
        if spending_ids:
            self.delete_spending(spending_ids)

    @staticmethod
    def raise_for_status(response: APIResponse):
        if not response.ok:
            raise Exception(f"{response.status}")
