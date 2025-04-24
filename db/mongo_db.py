# mongo_db.py
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient


MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "chat_db"


sync_client = MongoClient(MONGO_URL)
sync_db = sync_client[DB_NAME]


async_client = AsyncIOMotorClient(MONGO_URL)
async_db = async_client[DB_NAME]


#  Sync DB getter
def get_sync_mongo():
    try:
        yield sync_db
    finally:
        sync_client.close()

#  Async DB getter
async def get_async_mongo():
    try:
        yield async_db
    finally:
        async_client.close()  
