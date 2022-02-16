import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.util import await_only, greenlet_spawn

from sqlalchemy import Column, Table, ForeignKey, true
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER

from db import Base
from .user_tag import user_tag

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(INTEGER, primary_key=True)
    tag = Column(VARCHAR(255), nullable=False, unique=True)
    users = relationship("User",
        secondary="user_tag",
        back_populates="tags")
        # uselist=true