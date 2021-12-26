import os
import htmlmin
import aiofiles
from typing import List
import aiofiles
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse

app = FastAPI()

def assert_destination(foldername:str)->str:
    if not os.path.exists(foldername):
        os.mkdir(foldername)
    return foldername

async def save_file(files):
    for itm in files:
        itm.file.seek(0)
        destination = os.path.join(assert_destination('new_files'), itm.filename)
        async with aiofiles.open(destination, 'wb') as fl:
            stop = False
            while not stop:
                chunk = itm.file.read(5000)
                if not chunk:
                    stop = True
                else:
                    await fl.write(chunk)

@app.post("/upload/")
async def create_upload_files(bg: BackgroundTasks, files: List[UploadFile] = File(...)):
    bg.add_task(save_file, files)
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    async with aiofiles.open('dnodetemplate.html', 'r') as fl:
        txt = await fl.read()
    content = htmlmin.minify(txt, remove_comments=True, remove_empty_space=True)
    return HTMLResponse(content=content)