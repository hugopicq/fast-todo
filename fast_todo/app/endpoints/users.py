import logging

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query

from fast_todo.app.repos.user_repo import get_users_repo, UserRepo
from fast_todo.app.models.users import CreateUserRequest, LoginRequest, UserResponse, LoginResponse

from fast_todo.app.token.token_maker import TokenMaker, get_token_maker

import fast_todo.utils.password as password_utils

logger = logging.getLogger("uvicorn")

router = APIRouter()

@router.post("/signup", tags=["users"])
async def create_user(
    create_request: CreateUserRequest,
    pg_users_repo: Annotated[UserRepo, Depends(get_users_repo)],
) -> UserResponse:
    hash = password_utils.hash_password(create_request.password)

    try:
        user = await pg_users_repo.insert_user(create_request.email, create_request.name, hash)
    except Exception as e:
        logger.exception("Error while creating user %s", e.__class__.__name__)
        raise HTTPException(
            status_code=500, detail="Internal server error. Retry later."
        )

    return UserResponse(id=user.id, email=user.email, name=user.name)

@router.post("/login", tags=["users"])
async def login(
    request: LoginRequest,
    pg_users_repo: Annotated[UserRepo, Depends(get_users_repo)],
    token_maker: Annotated[TokenMaker, Depends(get_token_maker)],
) -> LoginResponse:
    
    try:
        user = await pg_users_repo.get_user_by_email(email=request.email)
    except Exception as e:
        #TODO: Handle no row
        logger.exception("Error while getting user %s", e.__class__.__name__)
        raise HTTPException(
            status_code=500, detail="Internal server error. Retry later."
        )

    if password_utils.chech_password(request.password, user.hashed_password) == False:
        raise HTTPException(status_code=403, detail="Invalid email or password")
    
    token = token_maker.create_token(user.id)

    return LoginResponse(access_token=token)