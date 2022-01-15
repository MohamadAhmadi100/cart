from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_USER = 'root'
    MONGO_PASS = 'qweasdQWEASD'
    MONGO_HOST = '200.100.100.223'
    MONGO_DB = "db_cart"


settings = Settings()
