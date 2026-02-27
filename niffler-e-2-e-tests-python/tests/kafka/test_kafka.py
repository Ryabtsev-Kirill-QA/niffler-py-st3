import json
import allure
from allure import step
from faker import Faker
from databases.userdata_db import UserdataDb
from models.user import UserName
from utils.waiters import wait_until_timeout


@allure.feature('Регистрация')
@allure.story('KAFKA')
class TestAuthRegistrationKafka:
    @allure.title('KAFKA: Сообщение с пользователем публикуется в Kafka после успешной регистрации')
    def test_message_should_be_produced_to_kafka_after_successful_registration(self, auth_client, kafka):
        username = Faker().user_name()
        password = Faker().password(special_chars=False)

        kafka.reset_offsets("users")

        topic_partitions = kafka.subscribe_listen_new_offsets("users")

        result = auth_client.register(username, password)
        assert result.status_code == 201

        event = kafka.consume_message(topic_partitions)

        with step("Сообщение из кафки существует"):
            assert event != '' and event != b''

        with step("Сообщение содержит данные о зарегистрированном пользователе"):
            UserName.model_validate(json.loads(event.decode('utf8')))
            assert json.loads(event.decode('utf8'))['username'] == username


@allure.feature('Регистрация')
@allure.story('KAFKA')
class TestProduceRegistrationUserKafka:
    @allure.title('KAFKA: После отправки сообщения о регистрации пользователя в Kafka, пользоватаель создается в БД')
    def test_registration_user_after_producing_message_in_kafka(self, auth_client, kafka, user_db: UserdataDb):
        username = Faker().user_name()

        with step("Отправить сообщение о регистрации нового пользователя в Kafka"):
            kafka.produce_message('users', username)

        with step("Ждем пока данные о пользователе запишутся в БД"):
            user_from_db = wait_until_timeout(user_db.get_user_by_username)(username)

        with step("Имя пользователя в БД совпадает с отправленным сообщением в Kafka"):
            assert user_from_db.username == username
