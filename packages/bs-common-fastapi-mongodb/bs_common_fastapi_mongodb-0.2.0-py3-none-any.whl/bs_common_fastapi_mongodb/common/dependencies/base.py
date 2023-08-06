import motor.motor_asyncio

from bs_common_fastapi_mongodb.common.config.base import MongoConfig
from fastapi import Query


async def get_db():
    db = motor.motor_asyncio.AsyncIOMotorClient(MongoConfig.MONGODB_URI)
    database = db[MongoConfig.MONGODB_DBNAME]
    try:
        yield database
    finally:
        db.close()


async def pagination_parameters(
    skip: int = Query(description=MongoConfig.APP_DESCRIPTION_SKIP, default=0),
    limit: int = Query(description=MongoConfig.APP_DESCRIPTION_LIMIT, default=MongoConfig.APP_MAX_LIMIT_VALUE)
):
    limit = MongoConfig.APP_MAX_LIMIT_VALUE if limit > MongoConfig.APP_MAX_LIMIT_VALUE else limit
    return {'skip': skip, 'limit': limit}


async def projection_parameters(
        fields: str | None = Query(description=MongoConfig.APP_DESCRIPTION_FIELDS, default=None)
):
    return {x.strip(): 1 for x in fields.split(',')} if fields is not None else None
