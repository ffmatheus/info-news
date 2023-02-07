from app.auth.bearer import JWTBearer

from app.config import start_db
from app.routes import news, auth

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await start_db()


app.include_router(news.router)
app.include_router(auth.router)
