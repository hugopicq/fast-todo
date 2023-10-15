from typing import Protocol, Generator

from fast_todo.app.pg_pool import PGPool
from fast_todo.app.models.users import UserRecord

class UserRepo(Protocol):
    """Repo for user manipulation"""

    async def insert_user(
        self, email: str, name: str, hashed_password: str
    ) -> UserRecord:
        ...

    async def get_user_by_email(
        self, email: str
    ) -> UserRecord | None:
        ...    

CREATE_USER_QUERY = """
    INSERT INTO "users" ("email", "name", "hashed_password")
    VALUES ($1, $2, $3)
    RETURNING id, name, email, hashed_password, created_at;
"""

GET_USER_BY_EMAIL_QUERY = """
    SELECT id, name, email, hashed_password, created_at
    FROM "users"
    WHERE email = $1;
"""

class PGUserRepo(UserRepo):
    """PostgreSQL implementation of UserRepo"""

    async def insert_user(self, email: str, name: str, hashed_password: str) -> UserRecord:
        async with PGPool.get_connection() as conn:
            user = await conn.fetchrow(CREATE_USER_QUERY, email, name, hashed_password)
        return UserRecord(**user)
    
    async def get_user_by_email(self, email: str) -> UserRecord | None:
        async with PGPool.get_connection() as conn:
            user = await conn.fetchrow(GET_USER_BY_EMAIL_QUERY, email)

        if user is None:
            return None
        
        return UserRecord(**user)

PG_USER_REPO = PGUserRepo()

def get_users_repo() -> Generator[UserRepo, None, None]:
    """Get the users repo."""
    yield PG_USER_REPO
