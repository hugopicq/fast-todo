from fastapi import Request, Depends, HTTPException
from typing import Annotated

from fast_todo.app.token.token_payload import TokenPayload
from fast_todo.app.token.token_maker import get_token_maker, TokenMaker

async def authenticate_token(request: Request, token_maker: Annotated[TokenMaker, Depends(get_token_maker)]) -> TokenPayload:
    """
    Dependency to authenticate user using and return token payload
    """

    auth_header = request.headers.get("authorization", "")
    if len(auth_header) == 0:
        raise HTTPException(status_code=401, detail="Invalid authorization token")
    
    auth_header_parts = auth_header.split()
    if len(auth_header_parts) != 2:
        raise HTTPException(status_code=401, detail="Invalid authorization token")
    
    if auth_header_parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization scheme, only bearer supported")
    
    token = auth_header_parts[1]

    token_payload = token_maker.decode_token(token)
    if token_payload is None:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
    
    return token_payload