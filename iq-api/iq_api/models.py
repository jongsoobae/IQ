from pydantic import BaseModel

from iq_api.utils import db


class Person(BaseModel):
    name: str
    questions: list = []


class Question(BaseModel):
    title: str
    content: str
