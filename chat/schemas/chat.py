from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import ConfigDict,Field
from typing_extensions import Annotated


class Chat(BaseModel):
    id: Optional[int] = None 
    
    chat_type: str  # Either "CHAT" or "GROUP"
    name: Optional[str] = None
    image: Optional[str] = None
    members: List[int]  
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    
# Member Model
class Member(BaseModel):
    chat_id: int  
    user_id: int 

    def __repr__(self):
        return f"Member(chat_id={self.chat_id}, user_id={self.user_id})"

# Message Model
class Message(BaseModel):
    id : int
    chat_id: int
    text: Optional[str] = None
    file: Optional[str] = None
    created_at: datetime = datetime.utcnow()
