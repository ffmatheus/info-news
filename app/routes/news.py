from fastapi import APIRouter, status, Body, Depends

from fastapi.encoders import jsonable_encoder

from app.models.news import News, NewsUpdate, Response

from app.repository.news import *

from app.auth.auth import AuthHandler

router = APIRouter()
auth_handler = AuthHandler()


@router.get(
    "/news",
    response_description="Retrieve all news",
    response_model=Response,
    tags=["NEWS"],
)
async def all_news(auth=Depends(auth_handler.auth_wrapper)):
    news = await retrieve_news()
    if not news:
        return {
            "status_code": 404,
            "response_type": "not found",
            "description": "Noticias nao encontradas!",
            "data": news,
        }
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Noticias encontradas com sucesso!",
        "data": news,
    }


@router.get(
    "/news/{id}",
    response_description="Search news",
    response_model=Response,
    tags=["NEWS"],
)
async def search_news(id: PydanticObjectId, auth=Depends(auth_handler.auth_wrapper)):
    news = await retrieve_unique_news(id)
    if news:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Noticia encontrada com sucesso!",
            "data": news,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Noticia nao existe",
    }


@router.post(
    "/news",
    response_description="Create a news",
    status_code=status.HTTP_201_CREATED,
    response_model=Response,
    tags=["NEWS"],
)
async def create_news(news: News = Body(...), auth=Depends(auth_handler.auth_wrapper)):
    created_news = await create_news_data(news)
    return {
        "status_code": 201,
        "response_type": "success",
        "description": "Noticia criada com sucesso!",
        "data": created_news,
    }


@router.put(
    "/news/{id}",
    response_description="Update a news",
    response_model=Response,
    tags=["NEWS"],
)
async def update_news(
    id: PydanticObjectId,
    news: NewsUpdate = Body(...),
    auth=Depends(auth_handler.auth_wrapper),
):
    updated_news = await update_news_data(id, news.dict())
    if updated_news:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Noticia com ID: {} atualizada com sucesso!".format(id),
            "data": updated_news,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Noticia nao encontrada",
        "data": False,
    }


@router.delete("/news/{id}", response_description="Delete a news", tags=["NEWS"])
async def delete_news(id: PydanticObjectId, auth=Depends(auth_handler.auth_wrapper)):
    deleted_news = await delete_news_data(id)
    if deleted_news:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Noticia excluida com sucesso!",
            "data": deleted_news,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Noticia nao encontrada",
        "data": False,
    }
