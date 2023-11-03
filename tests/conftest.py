import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from hw2_11.db.models import Base
from hw2_11.db.db import get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def session():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):

    def overrider_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = overrider_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def user():
    return {
        "username": "joedcvdc",
        "email": "jonik@gmail.com",
        "password": "567234"
    }
