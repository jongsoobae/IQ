import json
import logging
from typing import List

from bson import ObjectId
from databases import DatabaseURL
from fastapi import Depends, FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect


class Person(BaseModel):
    name: str
    date: str
    questions: list = []


class Question(BaseModel):
    title: str
    content: str


class DataBase:
    client: AsyncIOMotorClient = None


class Notifier:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            await self._notify(message)

    async def push(self, msg: str):
        await self.generator.asend(msg)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        print("connected")
        print(self.connections)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)
        print("removed")
        print(self.connections)

    async def _notify(self, message: str):
        living_connections = []
        while len(self.connections) > 0:
            # Looping like this is necessary in case a disconnection is handled
            # during await websocket.send_text(message)
            websocket = self.connections.pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections = living_connections


db = DataBase()
app = FastAPI()
notifier = Notifier()


async def get_database() -> AsyncIOMotorClient:
    return db.client


origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def connect_to_mongo():
    logging.info("connect to mongo...")
    url = str(DatabaseURL(f"mongodb://root:root@127.0.0.1:27018"))
    db.client = AsyncIOMotorClient(url, maxPoolSize=10, minPoolSize=1)
    logging.info("connected!!")


async def close_mongo_connection():
    logging.info("mongo connection closing...")
    logging.info("closed!!")


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


def get_item(row):
    row["id"] = str(row.pop("_id"))
    return row


async def get_questions_from_db(db: AsyncIOMotorClient):
    results = []
    rows = db.iqdb.iqdb.questions.find()

    async for row in rows:
        results.insert(0, get_item(row))

    return results


async def get_person_from_db(db: AsyncIOMotorClient, _id):
    return await db.iqdb.iqdb.persons.find_one({"_id": ObjectId(_id)})


async def get_persons_from_db(db: AsyncIOMotorClient):
    results = []
    rows = db.iqdb.iqdb.persons.find()

    async for row in rows:
        results.insert(0, get_item(row))

    return results


async def create_person(db: AsyncIOMotorClient, person: Person):
    questions = await get_questions_from_db(db)
    await db.iqdb.iqdb.persons.insert_one(
        {"name": person.name, "date": person.date, "questions": questions}
    )


async def delete_person(db, _id: str):
    await db.iqdb.iqdb.persons.delete_one({"_id": ObjectId(_id)})


async def update_person(db, _id: str, query):
    await db.iqdb.iqdb.persons.update_one({"_id": ObjectId(_id)}, {"$set": query})


async def create_question(db: AsyncIOMotorClient, question: Question):
    created = await db.iqdb.iqdb.questions.insert_one(
        {"title": question.title, "content": question.content}
    )
    await get_person_from_db(db, created.inserted_id)
    return await db.iqdb.iqdb.questions.find_one({"_id": created.inserted_id})


async def delete_question(db, _id: str):
    await db.iqdb.iqdb.questions.delete_one({"_id": ObjectId(_id)})


async def update_question(db, _id: str, question: Question):
    await db.iqdb.iqdb.questions.update_one(
        {"_id": ObjectId(_id)},
        {"$set": {"title": question.title, "content": question.content}},
    )


@app.get("/questions")
async def get_questions(db: AsyncIOMotorClient = Depends(get_database)):
    return await get_questions_from_db(db)


@app.get("/persons")
async def get_persons(db: AsyncIOMotorClient = Depends(get_database)):
    return await get_persons_from_db(db)


@app.post("/persons")
async def post_persons(person: Person, db: AsyncIOMotorClient = Depends(get_database)):
    await create_person(db, person)
    return {"msg": "created"}


@app.get("/persons/{_id}")
async def get_single_person(_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    return get_item(await get_person_from_db(db, _id))


@app.delete("/persons/{_id}")
async def delete_persons(_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    await delete_person(db, _id)
    return {"msg": "deleted"}


@app.post("/questions")
async def post_questions(
    question: Question, db: AsyncIOMotorClient = Depends(get_database)
):
    return {"msg": "created", "data": get_item(await create_question(db, question))}


@app.delete("/questions/{_id}")
async def delete_questions(_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    await delete_question(db, _id)
    return {"msg": "deleted"}


@app.put("/questions/{_id}")
async def update_questions(
    _id: str, question: Question, db: AsyncIOMotorClient = Depends(get_database)
):
    await update_question(db, _id, question)
    return {"msg": "updated"}


@app.put("questions/{_id}/asked")
async def update_question_asked(
    _id: str, asked: bool, db: AsyncIOMotorClient = Depends(get_database)
):
    await update_question(db, _id, {"asked": asked})
    return {"msg": "updated"}


@app.websocket("/person/{_id}/question/ws")
async def websocket_endpoint(
    websocket: WebSocket, _id: str, db: AsyncIOMotorClient = Depends(get_database)
):
    await notifier.connect(websocket)
    try:
        while True:
            data = json.loads(await websocket.receive_text())
            value = data["value"]
            qidx = data["qidx"]
            query = {f"questions.{qidx}.{k}": v for k, v in value.items()}
            await update_person(db, _id, query)
            await notifier.push(json.dumps(data))
    except WebSocketDisconnect as e:
        print("disconnected", e)
        notifier.remove(websocket)


@app.on_event("startup")
async def startup():
    # Prime the push notification generator
    await notifier.generator.asend(None)
    print(notifier.connections)
