import os
import aiohttp
import htmlmin
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from utils.file_managment import list_img_resources
from services.management import register_service_on_engine

target_directory = os.path.abspath('img_dummy')
video_directory = os.path.abspath('vid_dummy')

app = FastAPI()


@app.on_event("startup")
async def launch_checking():
    indexer_url = 'http://localhost:8000/register/'
    service_info = {
        "url": "http://miblog.com", 
        "ip": "127.0.0.1", "port": 7020, 
        "service_type": "gallery", 
        "owner": "jose", 
        "description": "servicio para ver tus fotos",
        "content": "bienvenido"
    }
    indx = await register_service_on_engine(indexer_url, service_info)


app.mount("/rs", StaticFiles(directory=target_directory), name="static")
app.mount("/vd", StaticFiles(directory=video_directory), name="static")

def render_content(template:str, prefix:str, directory:str)->str:
    env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True)
    template = env.get_template(template)
    listing = list_img_resources(directory)
    txt = template.render(resource_list=[f'/{prefix}/{a}' for a in listing])
    return htmlmin.minify(txt, remove_comments=True, remove_empty_space=True)

@app.get('/is_alive/')
async def status_check():
    return True


@app.get("/alt")
async def vid_gallery():
    content = render_content('v_gallery.html', 'vd', video_directory)
    return HTMLResponse(content=content)


@app.get("/")
async def img_gallery():
    content = render_content('n_gallery.html', 'rs', target_directory)
    return HTMLResponse(content=content)

