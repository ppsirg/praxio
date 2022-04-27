import os
import htmlmin
import aiofiles
import asyncio
from fastapi import FastAPI
from services.management import ServiceRegister, check_services, index_service
from fastapi.responses import HTMLResponse


app = FastAPI()
templatename = os.path.join('templates', 's_engine.html')


@app.on_event("startup")
async def launch_checking():
    lp = asyncio.get_event_loop()
    lp.create_task(check_services())


@app.post('/register/')
async def register_service(register:ServiceRegister):
    """Allow a external site to register to be indexed in for search.
    """
    result = await index_service(register)
    return result



@app.get('/search/')
def search_service(q:str):
    """Search in indexed services based on a queryset, can use
    url, owner, description and content to get matches to show.
    return a list of matches
    url: str
    description: str
    """
    print(q)
    return {
        'matches': [
            {'id': a, 'owner': f'{a} blog', 'url': f'http://{a}-blog.com', 'addr': '0.0.0.0:9000', 'description': f'something {a}'} 
            for a in range(10)]
        }


@app.get('/')
async def service_index():
    """Show app frontend"""
    async with aiofiles.open(templatename, 'r') as fl:
        txt = await fl.read()
    content = htmlmin.minify(txt, remove_comments=True, remove_empty_space=True)
    return HTMLResponse(content=content)




