import logging

from databases import DatabaseURL
from motor.motor_asyncio import AsyncIOMotorClient

from iq_api.settings import DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
from iq_api.utils import db


async def connect_to_mongo():
    logging.info("connect to mongo...")
    url = str(DatabaseURL(f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}"))
    db.client = AsyncIOMotorClient(url, maxPoolSize=10, minPoolSize=1)
    logging.info("connected!!")


async def close_mongo_connection():
    logging.info("mongo connection closing...")
    logging.info("closed!!")


async def startup():
    await connect_to_mongo()


async def shutdown():
    await close_mongo_connection()
