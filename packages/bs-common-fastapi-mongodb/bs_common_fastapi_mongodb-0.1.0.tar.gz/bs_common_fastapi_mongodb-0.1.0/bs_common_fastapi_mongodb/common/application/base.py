import datetime
from abc import abstractmethod

from bson.errors import InvalidId
from bson.objectid import ObjectId
from bs_common_fastapi.common.config.base import BaseConfig
from bs_common_fastapi.common.exception import NotFoundException, AppException
from pydantic.utils import deep_update


class BaseApplication:

    def __init__(self, db):
        self.__db = db
        self.__collection_name = None

    @property
    @abstractmethod
    def collection_name(self):
        raise NotImplementedError()

    @property
    def db(self):
        return self.__db

    @staticmethod
    def datetime_now(str_format: str = '%Y-%m-%d %H:%M:%S'):
        return datetime.datetime.now().strftime(str_format)

    @staticmethod
    def get_object_id(identifier: str) -> ObjectId:
        try:
            return ObjectId(identifier)
        except InvalidId as e:
            raise AppException(message=str(e))

    @staticmethod
    def clean_data(data: dict):
        data.pop('_id', None)
        return data

    async def find_all(
            self,
            limit: int = BaseConfig.APP_MAX_LIMIT_VALUE,
            skip: int = 0,
            query: dict | None = None,
            sort: dict | None = None,
            projection: dict | None = None
    ):
        q = {x: y for x, y in query.items()} if query is not None else {}
        projection = projection if projection is not None else {}
        obj = self.db.find(q, projection)
        if sort is not None:
            sort_list = []
            for key, value in sort.items():
                sort_list.append((key, value))
            obj = obj.sort(sort_list)
        obj = obj.skip(skip)
        return await obj.to_list(limit)

    async def find_one_by_identifier(
            self,
            identifier: str,
            projection: dict | None = None
    ):
        query = {'_id': self.get_object_id(identifier=identifier)}
        if (document := await self.db.find_one(query, projection)) is not None:
            return document
        raise NotFoundException(
            message=f'{self.collection_name.title()} with ID {identifier} not found'
        )

    async def find_one_by_field(
            self,
            field: str,
            value: str,
            projection: dict | None = None
    ):
        if (document := await self.db.find_one({field: value}, projection)) is not None:
            return document
        raise NotFoundException(
            message=f'{self.collection_name.title()} with {field} {value} not found'
        )

    async def create(
            self,
            data: dict
    ):
        data['created_at'] = self.datetime_now()
        data['updated_at'] = self.datetime_now()
        new_document = await self.db.insert_one(self.clean_data(data))
        return await self.find_one_by_identifier(identifier=new_document.inserted_id)

    async def update(
            self,
            identifier: str,
            data: dict
    ):
        updated_data = await self.find_one_by_identifier(identifier=identifier)
        data['updated_at'] = self.datetime_now()
        data = deep_update(updated_data, data)
        self.db.update_one({'_id': self.get_object_id(identifier=identifier)}, {'$set': self.clean_data(data)})
        return await self.find_one_by_identifier(identifier=identifier)

    async def delete(
            self,
            identifier: str
    ) -> bool:
        await self.find_one_by_identifier(identifier=identifier)
        delete_result = await self.db.delete_one({'_id': self.get_object_id(identifier=identifier)})

        if delete_result.deleted_count == 1:
            return True

        return False
