import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASS = os.getenv("MONGO_PASS")
    MONGO_HOST = os.getenv("MONGO_HOST")
    MONGO_PORT = int(os.getenv("MONGO_PORT"))

    APP_NAME = os.getenv("APP_NAME")

    RABBIT_HOST = os.getenv("RABBIT_HOST")
    RABBIT_PORT = int(os.getenv("RABBIT_PORT"))
    RABBIT_USER = os.getenv("RABBIT_PORT")
    RABBIT_PASS = os.getenv("RABBIT_PORT")



settings = Settings()
