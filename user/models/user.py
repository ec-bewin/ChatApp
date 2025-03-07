from sqlalchemy import Column, Integer, String
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True, unique=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True,nullable=True,)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
