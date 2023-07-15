from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    app_name: str = "Marketplace API"
    db_host: str = "localhost"
    db_port: str
    db_user: str
    db_pass: str
    db_name: str

    test_db_host: str = "localhost"
    test_db_port: str
    test_db_user: str
    test_db_pass: str
    test_db_name: str

    secret_key: SecretStr

    jwt_token_prefix: str = "Bearer"
    jwt_refresh_token_name: str = "refresh_token"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 25 * 7

    algorithm_jwt: str = "HS256"
    access_token_jwt_subject: str = "access"
    refresh_token_jwt_subject: str = "refresh"

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()