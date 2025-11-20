from playwright.sync_api import APIResponse


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

    def get_categories(self) -> dict:
        response = self.request_context.get("/api/categories/all")
        if not response.ok:
            raise Exception(f"{response.status}")
        return response.json()

    def add_category(self, name: str) -> dict:
        response = self.request_context.post("/api/categories/add", data={
            "category": name
        })
        if not response.ok:
            raise Exception(f"{response.status}")
        return response.json()

    def add_spends(self, body) -> dict:
        response = self.request_context.post("/api/spends/add", data=body)
        if not response.ok:
            raise Exception(f"{response.status}")
        return response.json()

    def get_all_spendings(self):
        response = self.request_context.get(
            "/api/v2/spends/all?page=0&searchQuery=&filterCurrency=&filterPeriod="
        )
        if not response.ok:
            raise Exception(f"{response.status}")
        return response

    def delete_spending(self, spending_id: str) -> APIResponse:
        response = self.request_context.delete(
            f"/api/spends/remove?ids={spending_id}"
        )
        if not response.ok:
            raise Exception(f"{response.status}")
        return response

    def delete_all_spendings(self):
        all_spendings = self.get_all_spendings()
        response_data = all_spendings.json()
        spendings = response_data.get('content', [])

        spending_ids = [spending['id'] for spending in spendings]

        if spending_ids:
            ids_param = ','.join(spending_ids)
            self.delete_spending(ids_param)
