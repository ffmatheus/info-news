from fastapi import APIRouter, HTTPException, Body
from app.auth.auth import AuthHandler
from app.models.auth import User, UserData, UserSignIn
from app.repository.auth import create_user


router = APIRouter()
auth_handler = AuthHandler()


@router.post("/register", response_model=UserData, tags=["AUTH"])
async def register_user(
    user: User = Body(...),
):
    user_exists = await User.find_one(User.email == user.email)
    if user_exists:
        raise HTTPException(status_code=409, detail="Email ja existe!")

    user.password = auth_handler.get_password_hash(user.password)
    new_user = await create_user(user)
    return new_user


@router.post("/login", tags=["AUTH"])
async def login(user_credentials: UserSignIn = Body(...)):
    user_exists = await User.find_one(User.email == user_credentials.username)
    if not user_exists or (
        not auth_handler.verify_password(
            user_credentials.password, user_exists.password
        )
    ):
        raise HTTPException(status_code=403, detail="Email ou senha incorretos!")
    token = auth_handler.encode_token(user_credentials.username)
    return {"token": token}
