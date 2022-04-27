import json
import os
import aiohttp
import htmlmin
import aiofiles
from typing import List
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from services.management import register_service_on_engine


app = FastAPI()
templatename = os.path.join('templates', 'c_chat.html')



@app.on_event("startup")
async def launch_checking():
    indexer_url = 'http://localhost:8000/register/'
    service_info = {
        "url": "http://miblog.com", 
        "ip": "127.0.0.1", "port": 7010, 
        "service_type": "chat", 
        "owner": "jose", 
        "description": "servicio para chatear con tus amigos",
        "content": "bienvenido"
    }
    indx = await register_service_on_engine(indexer_url, service_info)


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


@app.get('/is_alive/')
async def status_check():
    return True


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