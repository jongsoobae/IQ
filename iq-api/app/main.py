import json
from typing import List

from fastapi import Depends, FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

from app import mongo
from app.handlers import shutdown, startup
from app.models import Person, Question
from app.mongo.util import modify_id_response
from app.settings import CORS_ALLOWED
from app.utils import db, notifiers

app = FastAPI()


async def get_database() -> AsyncIOMotorClient:
    return db.client


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/questions")
async def get_questions(db: AsyncIOMotorClient = Depends(get_database)):
    return await mongo.question.find(db)


@app.get("/persons")
async def get_persons(db: AsyncIOMotorClient = Depends(get_database)):
    return await mongo.person.find(db)


@app.post("/persons")
async def post_persons(person: Person, db: AsyncIOMotorClient = Depends(get_database)):
    await mongo.person.insert_one(db, person)
    return {"msg": "created"}


@app.get("/persons/{_id}")
async def get_single_person(_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    return modify_id_response(await mongo.person.find_one(db, _id))


@app.delete("/persons/{_id}")
async def delete_persons(_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    await mongo.person.delete_one(db, _id)
    return {"msg": "deleted"}


@app.post("/questions")
async def post_questions(
    question: Question, db: AsyncIOMotorClient = Depends(get_database)
):
    tags = await mongo.tag.find(db)
    additional_tags = set(question.tags).difference(x["name"] for x in tags)
    await mongo.tag.insert_many(db, [{"name": tag} for tag in additional_tags])
    return {"msg": "created", "data": await mongo.question.insert_one(db, question)}


@app.delete("/questions/{_id}")
async def delete_questions(_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    await mongo.question.delete_one(db, _id)
    return {"msg": "deleted"}


@app.put("/questions/{_id}")
async def update_questions(
    _id: str, question: Question, db: AsyncIOMotorClient = Depends(get_database)
):
    tags = await mongo.tag.find(db)
    additional_tags = set(question.tags).difference(x["name"] for x in tags)
    await mongo.tag.insert_many(db, [{"name": tag} for tag in additional_tags])
    query = question.dict()
    await mongo.question.update_one(db, _id, query)
    return {"msg": "updated"}


@app.websocket("/person/{_id}/question/ws")
async def websocket_endpoint(
    websocket: WebSocket, _id: str, db: AsyncIOMotorClient = Depends(get_database)
):
    notifier = notifiers.get_notifier(_id)
    await notifier.connect(websocket)
    try:
        while True:
            data = json.loads(await websocket.receive_text())
            value = data["value"]
            qidx = data["qidx"]
            query = {f"questions.{qidx}.{k}": v for k, v in value.items()}
            await mongo.person.update_one(db, _id, query)
            await notifier._notify(json.dumps(data))
    except WebSocketDisconnect:
        print("disconnected", _id)
        if notifier.remove(websocket) == 0:
            notifiers.remove(_id)


@app.get("/tags")
async def get_tags(db: AsyncIOMotorClient = Depends(get_database)):
    return await mongo.tag.find(db)


@app.post("/tags")
async def post_tags(tags: List[str], db: AsyncIOMotorClient = Depends(get_database)):
    await mongo.tag.delete_all(db)
    if tags:
        await mongo.tag.insert_many(db, [{"name": tag} for tag in tags])
    return {"msg": "created"}


@app.delete("/tags/{name}")
async def delete_tags(name: str, db: AsyncIOMotorClient = Depends(get_database)):
    await mongo.tag.delete_by_name(db, name)
    return {"msg": "deleted"}
