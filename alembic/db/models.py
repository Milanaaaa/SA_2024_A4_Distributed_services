from sqlalchemy import Column, Integer, String
from alembic.db import DeclarativeBase



class User(DeclarativeBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
