import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASS = os.getenv("MONGO_PASS")
    MONGO_HOST = os.getenv("MONGO_HOST")
    MONGO_DB = os.getenv("MONGO_DB")

    APP_NAME = os.getenv("APP_NAME")

    RABBIT_HOST = os.getenv("RABBIT_HOST")


settings = Settings()
