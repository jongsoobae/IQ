from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from starlette.websockets import WebSocket


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

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)
        return len(self.connections)

    async def _notify(self, message: str):
        living_connections = []
        while self.connections:
            websocket = self.connections.pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections = living_connections


class Notifiers:
    notifiers = {}

    def get_notifier(self, _id) -> Notifier:
        if _id not in self.notifiers:
            self.notifiers[_id] = Notifier()
            self.notifiers[_id].generator.asend(None)
        return self.notifiers[_id]

    def remove(self, _id):
        del self.notifiers[_id]


db = DataBase()
notifiers = Notifiers()
