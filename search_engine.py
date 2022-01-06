import asyncio
from fastapi import FastAPI
from services.management import ServiceRegister, check_services

app = FastAPI()


@app.on_event("startup")
async def launch_checking():
    lp = asyncio.get_event_loop()
    lp.create_task(check_services())


@app.post('/register/')
def register_service(register:ServiceRegister):
    """Allow a external site to register to be indexed in for search.
    """
    pass


@app.get('/search/')
def search_service():
    """Search in indexed services based on a queryset, can use
    url, owner, description and content to get matches to show.
    return a list of matches
    url: str
    description: str
    """
    pass


@app.get('/')
def service_index():
    """Show app frontend"""
    pass




