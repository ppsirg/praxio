from fastapi import FastAPI
from services.management import register_service, ServiceRegisterOrder


app = FastAPI()


@app.post('/register/')
async def register_on_engine(register:ServiceRegisterOrder):
    return await register_service(register.indexer, register.resource)

@app.post('/note/')
async def create_note():
    pass

@app.post('/note/{note_id}/')
async def edit_note(note_id:int):
    pass

@app.delete('/note/{note_id}/')
async def delete_note(note_id:int):
    pass

@app.get('/note/')
async def list_notes():
    pass

@app.post('/note/{note_id}/')
async def get_note(note_id:int):
    pass

@app.get('/')
async def service_index():
    """Show app frontend"""
    pass


def register_on_browser():
    pass