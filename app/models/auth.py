from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class User(Document):
    fullname: str
    email: EmailStr
    password: str

    class Collection:
        name = "admin"

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Teste",
                "email": "example@example.com",
                "password": "@ex123",
            }
        }


class UserSignIn(HTTPBasicCredentials):
    class Config:
        schema_extra = {
            "example": {"username": "example@example.com", "password": "@ex123"}
        }


class UserData(BaseModel):
    fullname: str
    email: EmailStr

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Teste",
                "email": "example@example.com",
            }
        }
