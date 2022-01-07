import aiohttp
import asyncio
from enum import Enum
from pydantic import BaseModel
from typing import Optional
from settings import db as mongo

class ServiceType(Enum):
    blog= 'blog'
    chat= 'chat'
    browser= 'browser'
    gallery= 'gallery'
    upload= 'upload'
    dns= 'dns'


class ServiceRegister(BaseModel):
    """Third service register to be indexed and visible in
    search results.
    """
    url: Optional[str]
    ip: str
    port: int
    service_type: ServiceType
    owner: str
    description: str
    content: str


class ServiceRegisterOrder(BaseModel):
    indexer: Optional[str]
    resource: ServiceRegister


async def register_service(indexer_url:str, register:ServiceRegister):
    """Register a new service into search engine to be indexed"""
    async with aiohttp.ClientSession as cs:
        rw = await cs.post(indexer_url, data=register.json(), headers={'content-type': 'application/json'})


async def index_service(register:ServiceRegister):
    """Save register in search engine database to index it."""
    response = mongo['services'].insert_one(register.__dict__)
    return response


async def check_services():
    """Check services indexed to figure out if those are still alive"""
    services = []
    while True:
        for service in services:
            print(service) # in | motor  async no block petittions
        await asyncio.sleep(30)