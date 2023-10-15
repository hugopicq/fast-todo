from typing import Protocol, Generator

from fast_todo.app.models.tasks import TaskRecord
from fast_todo.app.pg_pool import PGPool

class TaskRepo(Protocol):
    """Repo for task manipulation"""

    async def insert_user_task(
        self, name: str, user_id: int, description: str = ""
    ) -> TaskRecord:
        ...

    async def list_user_tasks(
        self, user_id: int, last_id: int, limit: int
    ) -> list[TaskRecord]:
        ...

    async def delete_user_task(
        self, user_id: int, task_id: int
    ):
        ...

INSERT_USER_TASK_QUERY = """
    INSERT INTO "tasks" ("name", "description", "user_id")
    VALUES ($1, $2, $3)
    RETURNING id, name, description, created_at;
"""

LIST_USER_TASKS_QUERY = """
    SELECT id, name, description, created_at FROM "tasks"
    WHERE user_id = $1 AND id > $2
    ORDER BY id
    FETCH FIRST $3 ROWS ONLY
"""

DELETE_USER_TASK_QUERY = """
    DELETE FROM "tasks"
    WHERE user_id = $1 AND id = $2
"""

class PGTaskRepo(TaskRepo):
    
    async def insert_user_task(
        self, name: str, user_id: int, description: str = ""
    ) -> TaskRecord:
        async with PGPool.get_connection() as conn:
            task = await conn.fetchrow(INSERT_USER_TASK_QUERY, name, description, user_id)
        return TaskRecord(**dict(task))
    
    async def list_user_tasks(
        self, user_id: int, last_id: int, limit: int
    ) -> list[TaskRecord]:
        async with PGPool.get_connection() as conn:
            tasks = await conn.fetch(LIST_USER_TASKS_QUERY, user_id, last_id, limit)
        return [TaskRecord(**task) for task in tasks]
    
    async def delete_user_task(
        self, user_id: int, task_id: int
    ):
        async with PGPool.get_connection() as conn:
            await conn.execute(DELETE_USER_TASK_QUERY, user_id, task_id)

PG_TASK_REPO = PGTaskRepo()

def get_tasks_repo() -> Generator[TaskRepo, None, None]:
    """Get the tasks repo."""
    yield PG_TASK_REPO

