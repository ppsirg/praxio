import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from utils.file_managment import list_img_resources
from fastapi.middleware.cors import CORSMiddleware


base_dir = os.path.abspath(os.path.dirname(__file__))
target_directory = ''
prefix = 'dt'


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/dt", StaticFiles(directory=target_directory), name="static")


@app.get("/gallery/{folder}/")
async def img_gallery(folder:str):
    listing = list_img_resources(os.path.join(target_directory, folder))
    return [os.path.join(prefix, folder, a) for a in listing]


app.mount("/", StaticFiles(directory=os.path.join(base_dir, 'prx_fr', 'dist')), name="static")