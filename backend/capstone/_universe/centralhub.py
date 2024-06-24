import dataclasses
import os

import capstone._universe.wands.authentication
import capstone._universe.wands.dbengine
import capstone._universe.wands.query


class WandsCentralHub:
    def __init__(self, *, db_uri: str):
        self.__database_engine_wand = (
            capstone._universe.wands.dbengine.DatabaseEngineWand(self, db_uri=db_uri)
        )
        self.__authentication_wand = (
            capstone._universe.wands.authentication.AuthenticationWand(self)
        )
        self.__query_wand = capstone._universe.wands.query.QueryWand(self)

    @property
    def database_engine_wand(
        self,
    ) -> capstone._universe.wands.dbengine.DatabaseEngineWand:
        return self.__database_engine_wand

    @property
    def authentication_wand(
        self,
    ) -> capstone._universe.wands.authentication.AuthenticationWand:
        return self.__authentication_wand

    @property
    def query_wand(self) -> capstone._universe.wands.query.QueryWand:
        return self.__query_wand


def initialize_wch(*, database_uri: str = None):
    db_uri = database_uri or os.getenv("DATABASE_URI")
    if db_uri is None:
        raise ValueError("invalid SQL database URI.")
    import capstone.universe

    capstone.universe.universal_wch = WandsCentralHub(db_uri=db_uri)