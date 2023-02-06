from app.repository.auth import user_collection

# from fastapi import HTTPException, Depends, status
# from fastapi.security import HTTPBasicCredentials, HTTPBasic

# from passlib.context import CryptContext


# security = HTTPBasic()
# hash_helper = CryptContext(schemes=["bcrypt"])


# async def login(credentials: HTTPBasicCredentials = Depends(security)):
#     user = user_collection.find_one({"email": credentials.username})
#     if user:
#         password = hash_helper.verify(credentials.password, user["password"])
#         if not password:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Email ou senha incorretos",
#             )
#         return True
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos"
#     )

import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.config import Settings


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = Settings().secret_key

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=30),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
