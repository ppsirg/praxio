import os
import motor.motor_asyncio
from fastapi import FastAPI


app = FastAPI()

MONGODB_URL= os.environ.get("MONGODB_URL","mongodb://db:27017/db_name")    
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.college
