from app.auth.bearer import JWTBearer

from app.config import start_db
from app.routes import news, auth

from fastapi import FastAPI

app = FastAPI()

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await start_db()


app.include_router(news.router)
app.include_router(auth.router)
