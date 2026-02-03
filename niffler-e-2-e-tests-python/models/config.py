from pydantic import BaseModel


class Envs(BaseModel):
    frontend_url: str
    api_url: str
    auth_url: str
    spend_db_url: str
    userdata_db_url: str
    kafka_address: str
    niffler_username: str
    niffler_password: str
