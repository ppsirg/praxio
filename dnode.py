import aiofiles
import htmlmin
from typing import List
from utils.file_managment import save_file
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/upload/")
async def create_upload_files(bg: BackgroundTasks, files: List[UploadFile] = File(...)):
    bg.add_task(save_file, files)
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    async with aiofiles.open('n_upload.html', 'r') as fl:
        txt = await fl.read()
    content = htmlmin.minify(txt, remove_comments=True, remove_empty_space=True)
    return HTMLResponse(content=content)