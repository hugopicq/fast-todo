from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated
import logging

from fast_todo.app.models.tasks import ListTasksResponse, CreateTaskRequest, TaskRecord
from fast_todo.app.repos.task_repo import TaskRepo, get_tasks_repo
from fast_todo.app.dependencies import authenticate_token
from fast_todo.app.token.token_payload import TokenPayload

logger = logging.getLogger("uvicorn")

router = APIRouter()

@router.get("/tasks", tags=["tasks"])
async def list_tasks(
    pg_tasks_repo: Annotated[TaskRepo, Depends(get_tasks_repo)],
    token_payload: Annotated[TokenPayload, Depends(authenticate_token)],
    last_id: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> ListTasksResponse:
    """
    Lists tasks with a limit and starting at a certain index

    Parameters
    ----------
    pg_tasks_repo: instance of the tasks repository
    last_id: where to start listing (the last ID that was returned by the previous page)
    limit: how many results to return (max)

    Returns
    -------
    A list of tasks

    Raises
    ------
    HTTPException: 500 if there is a problem querying the database
    """

    try:
        tasks = await pg_tasks_repo.list_user_tasks(user_id=token_payload.user_id, last_id=last_id, limit=limit)
    except Exception as e:
        logger.exception("Error while listing tasks %s", e.__class__.__name__)
        raise HTTPException(
            status_code=500, detail="Internal server error. Retry later."
        )

    return ListTasksResponse(tasks=tasks)

@router.post("/tasks", tags=["tasks"])
async def create_task(
    task: CreateTaskRequest,
    pg_tasks_repo: Annotated[TaskRepo, Depends(get_tasks_repo)],
    token_payload: Annotated[TokenPayload, Depends(authenticate_token)],
) -> TaskRecord:
    """
    Create a task for a user

    Parameters
    ----------
    task: the task to create with name and description (optional) strings
    pg_tasks_repo: instance of the tasks repository

    Returns
    -------
    The created task with the id and the datetime of creation

    Raises
    ------
    HTTPException: 500 if there is a problem querying the database
    """

    try:
        created_task = await pg_tasks_repo.insert_user_task(task.name, token_payload.user_id, task.description)
    except Exception as e:
        logger.exception("Error while inserting task: %s", e.__class__.__name__)
        raise HTTPException(status_code=500, detail="Internal server error. Retry later.")
    
    return created_task

@router.delete("/tasks/{task_id}", tags=["tasks"])
async def delete_task(
    task_id: int,
    pg_tasks_repo: Annotated[TaskRepo, Depends(get_tasks_repo)],
    token_payload: Annotated[TokenPayload, Depends(authenticate_token)],
):
    """
    Delete a task for a user

    Parameters
    ----------
    task_id: the id of the task to delete
    pg_tasks_repo: instance of the tasks repository

    Returns
    -------
    None

    Raises
    ------
    HTTPException: 500 if there is a problem querying the database
    """

    try:
        await pg_tasks_repo.delete_task(token_payload.user_id, task_id)
    except Exception as e:
        logger.exception("Error while deleting task: %s", e.__class__.__name__)
        raise HTTPException(status_code=500, detail="Internal server error. Retry later.")