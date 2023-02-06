from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings

from app.models.news import News
from app.models.auth import User


class Settings(BaseSettings):

    # DATABASE URL
    DATABASE_URL: Optional[str] = None

    # SECURITY
    secret_key: str

    class Config:
        env_file = ".env"
        orm_mode = True


async def start_db():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(), document_models=[News, User]
    )
