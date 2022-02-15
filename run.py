import asyncio
from unicodedata import name

from sqlalchemy import Column, and_, update
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
from sqlalchemy.util import greenlet_spawn
from dal.a import A
from dal.b import B
from dal.tag import Tag
from dal.user import User
from dal.user_tag import user_tag

from datetime import datetime
from configs import db_conn_str

cur_timestamp = f'_{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'

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

    # tags = [Tag(tag="tag1"+cur_timestamp), Tag(tag="tag2"+cur_timestamp), Tag(tag="tag3"+cur_timestamp)]
    # users = [User(name="p1"+cur_timestamp), User(name="p2"+cur_timestamp), User(name="p3"+cur_timestamp)]

    # users[0].tags=[tags[0],tags[1]]
    # users[1].tags=[tags[0],tags[2]]
    
    async with async_session() as session:
        # async with session.begin():
        #     session.add_all(users)
        #     session.add_all(tags)

        # for user in users:
        #     await session.refresh(user)
        # for tag in tags:
        #     await session.refresh(tag)

        # for user in users:
        #     for i in range(3, user.id - 1, 1):
        #         await session.execute(user_tag.insert().values(user_id=user.id, tag_id=i))
        # await session.commit()
        
        # for i in range(1, 3):
        #     await session.execute(user_tag.insert().values(user_id=i, tag_id=i))
        # await session.commit()

        stmt1 = select(User).where(User.id == 1)
        result1 = await session.execute(stmt1)
        user1 = result1.scalars().one()
        print(f"user1 id =[{user1.id}]\n=================\n")

            # where(and_(user_tag.c.user_id == 26, user_tag.c.tag_id == 25)).
        stmt2 = (
            update(user_tag).
            where(user_tag.c.user_id == 23 and user_tag.c.tag_id == 23).
            values(tag_id = 1)
        )
        # stmt2 = (
        #     update(User).
        #     where(User.id == 26).
        #     values(name = "asdasd")
        # )
        await session.execute(stmt2)
        await session.commit()
        
        
        # await session.refresh(user1)

        # stmt = select(User).options(selectinload(User.tags))
        # result = await session.execute(stmt)
        # for cur_user in result.scalars():
        #     print(f"cur_user: {cur_user.id}")
        #     if cur_user.tags:
        #         tags = map(lambda u: str(u.id), cur_user.tags)
        #         tags_str = ';\n'.join(tags)
        #         print(f"with tags =[{tags_str}]\n=================\n")
    
    # tags = users[0].tags
    # # tags = await greenlet_spawn(users[0].tags)
    # print(tags)
    # print("done")

    # region
    # async with async_session() as session:
    #     async with session.begin():
    #         session.add_all(
    #             [
    #                 A(bs=[B(), B()], data="a1"),
    #                 A(bs=[B()], data="a2"),
    #                 A(bs=[B(), B()], data="a3"),
    #             ]
    #         )

    #     stmt = select(A).options(selectinload(A.bs))

    #     result = await session.execute(stmt)

    #     for a1 in result.scalars():
    #         print(a1)
    #         print(f"created at: {a1.create_date}")
    #         for b1 in a1.bs:
    #             print(b1)

    #     result = await session.execute(select(A).order_by(A.id))

    #     a1 = result.scalars().first()

    #     a1.data = "new data"

    #     await session.commit()

    #     # access attribute subsequent to commit; this is what
    #     # expire_on_commit=False allows
    #     print(a1.data)
    # endregion

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(async_main())