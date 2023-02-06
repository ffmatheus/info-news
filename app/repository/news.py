from typing import List, Union

from beanie import PydanticObjectId

from app.models.news import News

from typing import List, Union

news_collection = News


async def retrieve_news() -> List[News]:
    news = await news_collection.all().to_list()
    return news


async def retrieve_unique_news(id: PydanticObjectId) -> News:
    news = await news_collection.get(id)
    if news:
        return news


async def create_news_data(news: News) -> News:
    news = await news.create()
    return news


async def update_news_data(id: PydanticObjectId, data: dict) -> Union[bool, News]:
    data_items = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in data_items.items()}}
    news = await news_collection.get(id)
    if news:
        await news.update(update_query)
        return news
    return False


async def delete_news_data(id: PydanticObjectId) -> bool:
    news = await news_collection.get(id)
    if news:
        await news.delete()
        return True
