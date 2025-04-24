

from  chat.schemas import Chat
from typing import List, Optional
from fastapi import Depends
from datetime import datetime
from db import get_async_mongo



async def create_chat(
    members: List[int],
    name: Optional[str] = None,
    chat_type: Optional[str] = "chat",
     db=Depends(get_async_mongo)
):
    
    chat_data = {
        "chat_type": chat_type,
        "name": name,
        "members": members,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    chat_data["id"] = str(result.inserted_id)

    result = await db["chats"].insert_one(chat_data)
   

    return result
   
    