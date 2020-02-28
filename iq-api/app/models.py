from pydantic import BaseModel


class Person(BaseModel):
    name: str
    questions: list = []


class Question(BaseModel):
    title: str
    content: str
