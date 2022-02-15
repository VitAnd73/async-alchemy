import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.util import await_only, greenlet_spawn

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import VARCHAR, INTEGER

from db import Base

user_tag = Table('user_tag', Base.metadata,
    Column('user_id', INTEGER, ForeignKey('users.id'), primary_key=True),
    Column('tag_id', INTEGER, ForeignKey('tags.id'), primary_key=True)
)