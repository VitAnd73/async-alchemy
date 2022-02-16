from sqlalchemy import true
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from configs import db_conn_str
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
Base = declarative_base()
class DB:
    def __init__(self, conn_str = db_conn_str, echo = true):
        self.engine = create_async_engine(conn_str, echo=echo)
        self.async_session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
    async def dispose(self):
        await self.engine.dispose()
    async def __aenter__(self):
        return self.engine
    async def __aexit__(self, exc_type, exc_value, exc_tb):
        await self.engine.dispose()