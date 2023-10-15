import datetime
import time
import jwt
import os
from typing import Protocol, Generator

from fast_todo.app.token.token_payload import TokenPayload
from fast_todo.app.config import config

JWT_ALGORITHM = "HS256"

class TokenMaker(Protocol):
    def create_token(self, user_id: int, duration: datetime.timedelta = config.access_token_duration) -> str:
        ...

    def decode_token(self, token: str) -> TokenPayload | None:
        ...

class JWTTokenMaker(TokenMaker):
    def create_token(self, user_id: int, duration: datetime.timedelta = config.access_token_duration) -> str:
        issued_at = datetime.datetime.now()
        expires_at = issued_at + duration
        payload = TokenPayload(user_id=user_id, issued_at=issued_at.timestamp(), expired_at=expires_at.timestamp())

        return jwt.encode(payload=payload.model_dump(), key=config.token_signing_key, algorithm=JWT_ALGORITHM)
    
    def decode_token(self, token: str) -> TokenPayload | None:
        try:
            decoded_token_raw = jwt.decode(token, config.token_signing_key, algorithms=[JWT_ALGORITHM])
            decoded_token = TokenPayload(**decoded_token_raw)
            return decoded_token if decoded_token.expired_at > time.time() else None
        except:
            return None
        
TOKEN_MAKER = JWTTokenMaker()

def get_token_maker() -> Generator[TokenMaker, None, None]:
    yield TOKEN_MAKER