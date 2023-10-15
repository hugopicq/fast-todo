import time

from pydantic import BaseModel

class TokenPayload(BaseModel):
    user_id: int
    issued_at: float
    expired_at: float