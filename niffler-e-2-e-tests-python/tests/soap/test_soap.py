import allure
from allure import step
from xmlschema import XMLSchemaChildrenValidationError

from templates.read_templates import current_user_xml, xsd_response
from utils.soap_parser import parsed_result


@allure.feature('Профиль пользователя')
@allure.story('SOAP')
class TestSoap:
    @allure.title('SOAP: Получение информации о пользователе через SOAP')
    def test_current_user_info_by_soap(self, soap_session, envs):
        with step("Отправляем запрос на получение данных о существующем пользователе в системе"):
            response = soap_session.request('POST', '', data=current_user_xml(envs.niffler_username))
            assert response.status_code == 200

        with step("Валидируем полученный ответ согласно XSD схеме"):
            try:
                xsd_response('userResponse').validate(response.text)
            except XMLSchemaChildrenValidationError as xsd_e:
                raise AssertionError(xsd_e)

        with step("В ответе пришли данные по пользователю"):
            user_data = parsed_result(response.text)

            assert user_data['username'] == 'test_user'
            assert user_data['currency'] == 'RUB'
