from typing import List, Union

from app.models.auth import User

user_collection = User


async def create_user(new_user: User) -> User:
    user = await new_user.create()
    return user
