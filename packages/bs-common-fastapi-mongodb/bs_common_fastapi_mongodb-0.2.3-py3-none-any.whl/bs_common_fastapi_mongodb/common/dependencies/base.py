import motor.motor_asyncio

from bs_common_fastapi_mongodb.common.config.base import mongo_settings
from fastapi import Query


async def get_db():
    db = motor.motor_asyncio.AsyncIOMotorClient(mongo_settings.MONGODB_URI)
    database = db[mongo_settings.MONGODB_DBNAME]
    try:
        yield database
    finally:
        db.close()


async def pagination_parameters(
    skip: int = Query(description=mongo_settings.APP_DESCRIPTION_SKIP, default=0),
    limit: int = Query(description=mongo_settings.APP_DESCRIPTION_LIMIT, default=mongo_settings.APP_MAX_LIMIT_VALUE)
):
    limit = mongo_settings.APP_MAX_LIMIT_VALUE if limit > mongo_settings.APP_MAX_LIMIT_VALUE else limit
    return {'skip': skip, 'limit': limit}


async def projection_parameters(
        fields: str | None = Query(description=mongo_settings.APP_DESCRIPTION_FIELDS, default=None)
):
    return {x.strip(): 1 for x in fields.split(',')} if fields is not None else None
