from typing import List

from bson.objectid import ObjectId

from app.models import Question
from app.mongo.util import modify_id_response


def model(db):
    return db.iqdb.questions


async def find(db):
    rows = model(db).find().sort("_id", -1)
    return [modify_id_response(row) async for row in rows]


async def insert_one(db, question: Question):
    created = await model(db).insert_one(question.dict())
    return modify_id_response(await model(db).find_one({"_id": created.inserted_id}))


async def update_one(db, _id: str, query):
    await model(db).update_one(
        {"_id": ObjectId(_id)}, {"$set": query},
    )


async def delete_one(db, _id: str):
    await model(db).delete_one({"_id": ObjectId(_id)})


async def update_tag(db, _id: str, tags: List[str]):
    await model(db).update_one({"_id": ObjectId(_id)}, {"$set": {"tags": tags}})
