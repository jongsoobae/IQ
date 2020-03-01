from bson.objectid import ObjectId

from app.models import Question


def get_item(row):
    row["id"] = str(row.pop("_id"))
    return row


def model(db):
    return db.iqdb.questions


async def find(db):
    rows = model(db).find().sort("_id", -1)
    return [get_item(row) async for row in rows]


async def insert_one(db, question: Question):
    created = await model(db).insert_one(
        {"title": question.title, "content": question.content}
    )
    return await get_item(model(db).find_one({"_id": created.inserted_id}))


async def update_one(db, _id: str, query):
    await model(db).update_one(
        {"_id": ObjectId(_id)}, {"$set": query},
    )


async def delete_one(db, _id: str):
    await model(db).delete_one({"_id": ObjectId(_id)})
