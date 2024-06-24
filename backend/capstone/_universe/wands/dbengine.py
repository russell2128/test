import dataclasses
import asyncio
from collections.abc import Iterable

import sqlalchemy.ext.asyncio.engine
import sqlalchemy.orm
import sqlmodel
import sqlmodel.ext.asyncio.session

import capstone._universe.wands


class DatabaseEngineWand(capstone._universe.wands.AbstractBaseWand):
    def __init__(self, central_hub_, *, db_uri: str):
        super().__init__(central_hub_)
        self.__async_database_engine = (
            sqlalchemy.ext.asyncio.engine.create_async_engine(
                db_uri, echo=True, future=True
            )
        )

        asyncio.run(self._metadata_create_all())

    async def _metadata_create_all(self):
        async with self.__async_database_engine.begin() as conn:
            conn: sqlalchemy.ext.asyncio.engine.AsyncConnection
            await conn.run_sync(sqlmodel.SQLModel.metadata.create_all)

    async def async_session(self) -> sqlmodel.ext.asyncio.session.AsyncSession:
        return sqlmodel.ext.asyncio.session.AsyncSession(self.__async_database_engine)

    def session(self) -> sqlmodel.Session:
        return sqlmodel.Session(self.__async_database_engine.engine)

    async def insert_items(self, items: Iterable[sqlmodel.SQLModel]):
        with self.async_session() as a_session:
            a_session: sqlmodel.ext.asyncio.session.AsyncSession
            a_session.add_all(items)
            await a_session.commit()

    async def insert_item(self, item: sqlmodel.SQLModel):
        with self.async_session() as a_session:
            a_session: sqlmodel.ext.asyncio.session.AsyncSession
            a_session.add(item)
            await a_session.commit()