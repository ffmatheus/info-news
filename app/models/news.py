from beanie import Document

import datetime

from pydantic import BaseModel, Field

from typing import Optional, Any


class News(Document):
    tittle: str
    content: str
    date_insert: datetime.datetime

    class Config:
        schema_extra = {
            "example": {
                "tittle": "example@ex.com",
                "content": "example",
                "date_insert": "2022-02-02 00:00:00",
            }
        }


class NewsUpdate(BaseModel):
    tittle: Optional[str]
    content: Optional[str]
    date_insert: Optional[datetime.datetime]

    class Collection:
        name = "news"

    class Config:
        schema_extra = {
            "example": {
                "tittle": "example@ex.com",
                "content": "example",
                "date_insert": "2022-02-02 00:00:00",
            }
        }


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "description",
                "data": "data",
            }
        }
