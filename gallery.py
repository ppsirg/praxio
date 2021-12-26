import os
import htmlmin
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from utils.file_managment import list_img_resources

target_directory = os.path.abspath('img_dummy')
app = FastAPI()
app.mount("/rs", StaticFiles(directory=target_directory), name="static")

def render_content():
    env = Environment(loader=FileSystemLoader('templates'), trim_blocks=True)
    template = env.get_template('n_gallery.html')
    listing = list_img_resources(target_directory)
    txt = template.render(resource_list=[f'/rs/{a}' for a in listing])
    return htmlmin.minify(txt, remove_comments=True, remove_empty_space=True)

content = render_content()

@app.get("/")
async def main():
    return HTMLResponse(content=content)