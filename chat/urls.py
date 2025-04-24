from fastapi import APIRouter, HTTPException

from chat.cruds import create_chat
from chat.schemas import Chat
router = APIRouter()
from typing import List, Optional
from fastapi import Depends
from db import get_async_mongo

@router.post("/chats/")
async def create_chat_route(
    chat_data: Chat,  # The request body that FastAPI will parse into a ChatCreateRequest object
    db=Depends(get_async_mongo)  # Dependency to get the async MongoDB connection
):
    try:
        # Call the create_chat function and pass the necessary data
        chat = await create_chat(
            members=chat_data.members, 
            name=chat_data.name, 
            chat_type=chat_data.chat_type, 
            db=db
        )
        return chat  # Return the chat data as a response
    except Exception as e:
        # Catch any exception and raise an HTTPException to return an error message
        raise HTTPException(status_code=400, detail=str(e))