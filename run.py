import asyncio

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import sessionmaker
from dal.a import A
from dal.b import B

from db import Base
from datetime import datetime
from configs import db_conn_str

cur_timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

async def async_main():
    engine = create_async_engine(
        db_conn_str,
        echo=True,
    )

    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    A(bs=[B(), B()], data="a1"),
                    A(bs=[B()], data="a2"),
                    A(bs=[B(), B()], data="a3"),
                ]
            )

        stmt = select(A).options(selectinload(A.bs))

        result = await session.execute(stmt)

        for a1 in result.scalars():
            print(a1)
            print(f"created at: {a1.create_date}")
            for b1 in a1.bs:
                print(b1)

        result = await session.execute(select(A).order_by(A.id))

        a1 = result.scalars().first()

        a1.data = "new data"

        await session.commit()

        # access attribute subsequent to commit; this is what
        # expire_on_commit=False allows
        print(a1.data)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(async_main())