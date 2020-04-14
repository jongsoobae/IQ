from bson.objectid import ObjectId

from app.models import Person
from app.mongo import question
from app.mongo.util import modify_id_response


def model(db):
    return db.iqdb.persons


async def find(db):
    rows = model(db).find().sort("_id", -1)
    return [modify_id_response(row) async for row in rows]


async def find_one(db, _id):
    return await model(db).find_one({"_id": ObjectId(_id)})


async def insert_one(db, person: Person):
    questions = await question.find(db)
    await model(db).insert_one({"name": person.name, "questions": questions})


async def update_one(db, _id: str, query):
    await model(db).update_one({"_id": ObjectId(_id)}, {"$set": query})


async def delete_one(db, _id: str):
    await model(db).delete_one({"_id": ObjectId(_id)})
