import aiohttp
import asyncio
from enum import Enum
from pydantic import BaseModel
from typing import Optional


class ServiceType(Enum):
    blog= 'blog'
    chat= 'chat'
    browser= 'browser'
    gallery= 'gallery'
    cloud= 'cloud'
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
    is_active: Optional[bool] = True
    id: Optional[str]



indexed_services = []


async def register_service_on_engine(indexer_url:str, service_info:dict):
    """Register a new service into search engine to be indexed"""
    async with aiohttp.ClientSession() as cs:
        rw = await cs.post(indexer_url, json=service_info)
        if rw.status not in (200, 201):
            failure_detail = await rw.text()
            print(rw.status, failure_detail)
            return None
        else:
            print('indexed success',  rw.status)
            return await rw.json()


async def index_service(register:ServiceRegister):
    """Save register in search engine database to index it."""
    new_service = register.dict()
    indexed_services.append(new_service)
    # todo: implement dns register and return dns
    return f'{register.ip}:{register.port}'


async def check_services():
    """Check services indexed to figure out if those are still alive"""
    services = indexed_services
    while True:
        async with aiohttp.ClientSession() as cs:
            for service in services:
                try:
                    rw = await cs.get('http://{ip}:{port}/is_alive/'.format(**service))
                    if rw.status in (200, 201):
                        print('on ->', service)
                    else:
                        print('off ->', service)
                except Exception as err:
                    print('down ->', service)
        await asyncio.sleep(10)