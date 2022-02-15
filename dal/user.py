import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.util import await_only, greenlet_spawn

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER

from db import Base
from .user_tag import user_tag

class User(Base):
    __tablename__ = 'users'
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(32), nullable=False, unique=True)
    
    tags = relationship("Tag",
        secondary="user_tag",
        back_populates="users")