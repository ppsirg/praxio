import os
import htmlmin
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from utils.file_managment import list_img_resources

target_directory = os.path.abspath('img_dummy')
video_directory = os.path.abspath('vid_dummy')

app = FastAPI()
app.mount("/rs", StaticFiles(directory=target_directory), name="static")
app.mount("/vd", StaticFiles(directory=video_directory), name="static")

def render_content(template:str, prefix:str, directory:str)->str:
    env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True)
    template = env.get_template(template)
    listing = list_img_resources(directory)
    txt = template.render(resource_list=[f'/{prefix}/{a}' for a in listing])
    return htmlmin.minify(txt, remove_comments=True, remove_empty_space=True)


@app.get("/")
async def img_gallery():
    content = render_content('n_gallery.html', 'rs', target_directory)
    return HTMLResponse(content=content)

@app.get("/alt")
async def vid_gallery():
    content = render_content('v_gallery.html', 'vd', video_directory)
    return HTMLResponse(content=content)