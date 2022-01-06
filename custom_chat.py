import os
import htmlmin
import aiofiles
from typing import List
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from services.management import register_service, ServiceRegisterOrder


app = FastAPI()
templatename = os.path.join('templates', 'c_chat.html')


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_text(data)


manager = ConnectionManager()

@app.post('/register/')
async def register_on_engine(register:ServiceRegisterOrder):
    return await register_service(register.indexer, register.resource)


@app.websocket('/chat/{client_id}/', name='chat_session')
async def chat_session(ws:WebSocket, client_id:int):
    await manager.connect(ws)
    while True:
        data = await ws.receive_text()
        await manager.broadcast(f"Client {client_id}: {data}")


@app.get('/')
async def service_index():
    """Show app frontend"""
    async with aiofiles.open(templatename, 'r') as fl:
        txt = await fl.read()
    content = htmlmin.minify(txt, remove_comments=True, remove_empty_space=True)
    return HTMLResponse(content=content)