import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.db_handlers.session import get_db
from app.root.utils.abstract_base import AbstractBase

# SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    AbstractBase.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        AbstractBase.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_auth_and_onboarding(client):
    # Register
    response = client.post(
        "/auth/register",
        json={
            "email": "owner@example.com",
            "password": "secretpassword",
            "first_name": "Owner",
            "last_name": "SaaS"
        }
    )
    assert response.status_code == 200

    # Login
    response = client.post(
        "/auth/login",
        data={"username": "owner@example.com", "password": "secretpassword"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Onboard Tenant
    response = client.post(
        "/tenants/",
        json={
            "company_name": "Acme Corp",
            "schema_name": "acme_schema",
            "company_size": 10
        },
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["company_name"] == "Acme Corp"
