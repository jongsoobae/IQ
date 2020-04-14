from typing import List

from bson.objectid import ObjectId

from app.models import Tag
from app.mongo.util import modify_id_response


def model(db):
    return db.iqdb.tags


async def find(db):
    rows = model(db).find().sort("_id", -1)
    return [modify_id_response(row) async for row in rows]


async def find_one(db, _id):
    return await model(db).find_one({"_id": ObjectId(_id)})


async def insert_one(db, tag: Tag):
    await model(db).insert_one({"name": tag.name})


async def delete_all(db):
    await model(db).delete_many({})


async def insert_many(db, tags: List[Tag]):
    await model(db).insert_many(tags)


async def update_one(db, _id: str, query):
    await model(db).update_one({"_id": ObjectId(_id)}, {"$set": query})


async def delete_one(db, _id: str):
    await model(db).delete_one({"_id": ObjectId(_id)})


async def delete_by_name(db, name: str):
    await model(db).delete_one({"name": name})
