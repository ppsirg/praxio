import aiofiles
import htmlmin
from typing import List
from utils.file_managment import save_file
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse
from services.management import register_service_on_engine

app = FastAPI()


@app.on_event("startup")
async def launch_checking():
    indexer_url = 'http://localhost:8000/register/'
    service_info = {
        "url": "http://miblog.com", 
        "ip": "127.0.0.1", "port": 7030, 
        "service_type": "cloud", 
        "owner": "jose", 
        "description": "servicio para chatear con tus amigos",
        "content": "bienvenido"
    }
    indx = await register_service_on_engine(indexer_url, service_info)


@app.post("/upload/")
async def create_upload_files(bg: BackgroundTasks, files: List[UploadFile] = File(...)):
    bg.add_task(save_file, files)
    return {"filenames": [file.filename for file in files]}


@app.get('/is_alive/')
async def status_check():
    return True


@app.get("/")
async def main():
    async with aiofiles.open('n_upload.html', 'r') as fl:
        txt = await fl.read()
    content = htmlmin.minify(txt, remove_comments=True, remove_empty_space=True)
    return HTMLResponse(content=content)