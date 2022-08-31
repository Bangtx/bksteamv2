import pytest
from main import app
from fastapi.testclient import TestClient
from config.setting import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT, \
    POSTGRES_USER, POSTGRES_PASSWORD
from utils import auth
from alembic.config import Config
from alembic import command


@pytest.fixture(scope="function")
def db():
    from config.database import db, bare_cursor

    test_database = f"{POSTGRES_DB}_test"

    db.close()
    db.database = "postgres"
    with bare_cursor(db) as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {test_database}")
        cursor.execute(f"CREATE DATABASE {test_database}")
    db.close()

    db.database = test_database
    yield db


@pytest.fixture(scope="function")
def migrate():
    # Run migrate
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}_test"
    )
    command.upgrade(alembic_cfg, "head")


@pytest.fixture(scope="session")
def token():
    # Add a fake token
    token = auth.generate_token(email="cut@grower.com")
    yield token


@pytest.fixture(scope="function")
def client(db, token, migrate):
    app.state._db = db
    client = TestClient(app)
    client.headers = {"Authorization": f"Bearer {token}"}
    yield client
