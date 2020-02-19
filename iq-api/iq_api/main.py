import logging
import pprint
from datetime import date

from databases import DatabaseURL
from fastapi import Depends, FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class Person(BaseModel):
    name: str
    date: str
    questions: list = []


class DataBase:
    client: AsyncIOMotorClient = None


db = DataBase()
app = FastAPI()


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


contents = [
    """
python dict 의 time complexity 는?
- O(1)
    """,
    """
세션과 쿠키의 차이가 무엇인지 설명하시오.
- 세션은 서버에 저장되는 정보.
- 쿠키는 클라이언트에 저장되는 정보.
    """,
    """
세션방식의 인증과 토큰 방식의 인증 의 차이를 설명하시오.
- 세션방식은 서버에 세션정보를 저장해놓고 매 request 마다 sessionid 가 존재하는지 체크함.
    - revoke 가능, stateless 하지 않음.
    - stateless (서버 scaleout 용이), revoke 불가.
    """,
    """
python GIL 에 대해서 설명하시오. (cpython 한정)
- 여러 쓰레드가 하나의 python object 에 동시에 접근하지 못하게 하는것.
GIL 의 장단점은?
- 장점: cpython 구현이 용이.
- 단점: 쓰레드 대신 프로세스 를 쓰는것에 대한 이야기.
    """,
]


async def get_questions_from_db(db: AsyncIOMotorClient):
    results = []
    rows = db.iqdb.iqdb.questions.find()

    async for row in rows:
        row.update({"_id": str(row["_id"])})
        results.append(row)

    return results


async def get_persons_from_db(db: AsyncIOMotorClient):
    results = []
    rows = db.iqdb.iqdb.persons.find()

    async for row in rows:
        row.update({"_id": str(row["_id"])})
        results.append(row)

    return results


async def create_person(db: AsyncIOMotorClient, person: Person):
    await db.iqdb.iqdb.persons.insert_one({"name": person.name, "date": person.date})


async def delete_person(db, name: str):
    await db.iqdb.iqdb.persons.delete_one({"name": name})


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


@app.delete("/persons/{name}")
async def delete_persons(name: str, db: AsyncIOMotorClient = Depends(get_database)):
    await delete_person(db, name)
    return {"msg": "deleted"}
