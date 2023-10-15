import datetime
import os
from dotenv import load_dotenv
from pathlib import Path


class _Config():
    token_signing_key: str
    access_token_duration: datetime.timedelta
    postgres_dsn: str
    asyncpg_min_pool_size: int
    asyncpg_max_pool_size: int

    def __init__(self):
        load_dotenv(dotenv_path=Path("docker/app.env"))
        self.token_signing_key = os.getenv("TOKEN_SIGNING_KEY")
        self.access_token_duration = datetime.timedelta(minutes=int(os.getenv("ACCESS_TOKEN_DURATION_MINUTES")))
        self.postgres_dsn = (os.getenv("POSTGRES_DSN") or "postgresql://root:secret@localhost:5432/fasttodo")
        self.asyncpg_min_pool_size = int(os.getenv("ASYNCPG_MIN_POOL_SIZE", 1))
        self.asyncpg_max_pool_size = int(os.getenv("ASYNCPG_MAX_POOL_SIZE", 1))

config = _Config()