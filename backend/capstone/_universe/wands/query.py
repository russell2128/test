import sqlmodel

import capstone._universe.wands
import capstone.data.dbtable


class QueryWand(capstone._universe.wands.AbstractBaseWand):
    def __init__(self, central_hub_):
        super().__init__(central_hub_)

    async def lookup_user(self, username: str) -> capstone.data.dbtable.User | None:
        async with self.master_central_hub.database_engine_wand.async_session() as a_session:
            statement = sqlmodel.select(capstone.data.dbtable.User).where(
                capstone.data.dbtable.User.username == username
            )
            result = list(await a_session.exec(statement))
            if len(result) == 0:
                return None
            else:
                return result[0]

    async def is_email_already_taken(self, email: str) -> bool:
        async with self.master_central_hub.database_engine_wand.async_session() as a_session:
            statement = sqlmodel.select(capstone.data.dbtable.User).where(
                capstone.data.dbtable.User.email == email
            )
            result = await a_session.exec(statement)
            return len(list(result)) > 0