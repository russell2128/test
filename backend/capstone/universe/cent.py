import dataclasses
import os

import sqlmodel

import capstone.universe.auth
import capstone.universe.db


@dataclasses.dataclass
class WandsCentralHub:
    auth_wand: capstone.universe.auth.AuthenticationWand
    db_wand: capstone.universe.db.DatabaseWand

    def db_session(self) -> sqlmodel.Session:
        return self.db_wand.session()


universal_wch: WandsCentralHub


def initialize_wch():
    global universal_wch
    db_uri = os.getenv("DATABASE_URI")
    if db_uri is None:
        raise ValueError("invalid SQL database URI.")

    db_wand = capstone.universe.db.DatabaseWand(
        sqlmodel.create_engine(url=db_uri, echo=True)
    )

    universal_wch = WandsCentralHub(
        auth_wand=capstone.universe.auth.AuthenticationWand(), db_wand=db_wand
    )
    sqlmodel.SQLModel.metadata.create_all(universal_wch.db_wand.database_engine)
