from fast_todo.app.app import app
from fastapi.testclient import TestClient
from fast_todo.app.repos.user_repo import get_users_repo, UserRepo
from fast_todo.app.models.users import UserRecord
from fast_todo.utils.random import random_string
from fast_todo.utils.password import hash_password
import random
import datetime

# def random_user(password: str) -> UserRecord:
#     return UserRecord(id=random.randint(1, 5000), name=random_string(10), email=f"{random_string(8)}@gmail.com", hashed_password=hash_password(password), created_at=datetime.datetime.now())

MOCK_PASSWORD = "Mypassword123"

class MockUserRepo(UserRepo):
    """Mock implementation of the user repo"""

    async def insert_user(self, email: str, name: str, hashed_password: str) -> UserRecord:
        return UserRecord(id=random.randint(1, 5000), name=name, email=email, hashed_password=hashed_password, created_at=datetime.datetime.now())
    
    async def get_user_by_email(self, email: str) -> UserRecord | None:
        return UserRecord(id=random.randint(1, 5000), name=random_string(10), email=email, hashed_password=hash_password(MOCK_PASSWORD), created_at=datetime.datetime.now())
    
async def override_get_user_repo():
    return MockUserRepo()

def test_create_user():
    client = TestClient(app)
    app.dependency_overrides[get_users_repo] = override_get_user_repo

    email = f"{random_string(8)}@gmail.com"
    name = random_string(8)
    password = "Totototo123!"
    

    response = client.post(
        "/signup",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200
    resp = response.json()
    assert resp["id"] > 0
    assert resp["name"] == name
    assert resp["email"] == email
    
    response = client.post(
        "/signup",
        json={
            "name": name,
            "email": email,
            "password": "nostrong"
        }
    )

    assert response.status_code >= 400

def test_login_user():
    client = TestClient(app)

    response = client.post(
        "/login",
        json={
            "email": f"{random_string(8)}@gmail.com",
            "password": MOCK_PASSWORD,
        }
    )

    assert response.status_code == 200
    resp = response.json()
    assert resp["access_token"] is not None

    response = client.post(
        "/login",
        json={
            "email": f"{random_string(8)}@gmail.com",
            "password": MOCK_PASSWORD + "aze",
        }
    )

    assert response.status_code == 403