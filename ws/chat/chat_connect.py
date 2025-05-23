from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, chat_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, chat_id: str, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, chat_id: str, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
