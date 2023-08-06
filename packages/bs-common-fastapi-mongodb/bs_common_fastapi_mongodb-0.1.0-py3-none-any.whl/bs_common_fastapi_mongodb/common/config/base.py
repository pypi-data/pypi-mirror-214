import os
from bs_common_fastapi.common.config.base import BaseConfig


class MongoConfig(BaseConfig):
    MONGODB_HOST: str = os.getenv('MONGODB_HOST')
    MONGODB_USER: str = os.getenv('MONGODB_USER')
    MONGODB_PASS: str = os.getenv('MONGODB_PASS')
    MONGODB_DBNAME: str = os.getenv('MONGODB_DBNAME')
    MONGODB_DRIVER: str = os.getenv('MONGODB_DRIVER')
    MONGODB_ARGS: str = os.getenv('MONGODB_ARGS')
    MONGODB_URI: str = f'{MONGODB_DRIVER}://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_HOST}/{MONGODB_ARGS}'
