import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

_env = os.environ.get

POSTGRES_DB = _env("POSTGRES_DB")
POSTGRES_HOST = _env("POSTGRES_HOST")
POSTGRES_USER = _env("POSTGRES_USER")
POSTGRES_PASSWORD = _env("POSTGRES_PASSWORD")
POSTGRES_PORT = _env("POSTGRES_PORT")

APP_ENV = _env("APP_ENV")
WEB_URL = _env("WEB_URL")
# API_INVOICE_URL = _env("API_INVOICE_URL")
PROJECT_NAME = _env("PROJECT_NAME")
LANGUAGE = _env("LANGUAGE")