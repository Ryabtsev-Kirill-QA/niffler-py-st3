import os
from playwright.sync_api import Playwright, APIResponse


class ApiMethods:
    def get_all_spendings(self, playwright: Playwright, get_token_from_user_state: str) -> APIResponse:
        api_url = os.getenv('API_URL')
        request_context = playwright.request.new_context(
            base_url=api_url,
            extra_http_headers={'Authorization': f'Bearer {get_token_from_user_state}'})

        response = request_context.get(
            "/api/v2/spends/all?page=0&searchQuery=&filterCurrency=&filterPeriod="
        )
        return response

    def delete_spending(self, playwright: Playwright, get_token_from_user_state: str, spending_id: str) -> APIResponse:
        api_url = os.getenv('API_URL')
        request_context = playwright.request.new_context(
            base_url=api_url,
            extra_http_headers={
                'Authorization': f'Bearer {get_token_from_user_state}'})

        response = request_context.delete(
            f"/api/spends/remove?ids={spending_id}"
        )
        return response

    def delete_all_spendings(self, playwright: Playwright, get_token_from_user_state: str):
        get_response = self.get_all_spendings(playwright, get_token_from_user_state)

        response_data = get_response.json()
        spendings = response_data.get('content', [])

        spending_ids = [spending['id'] for spending in spendings]

        if spending_ids:
            ids_param = ','.join(spending_ids)
            self.delete_spending(playwright, get_token_from_user_state, ids_param)
        return len(spending_ids)
