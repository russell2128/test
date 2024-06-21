import dataclasses

import pydantic
import sqlmodel
import sqlalchemy.engine


@dataclasses.dataclass
class DatabaseWand:
    database_engine: sqlalchemy.engine.Engine

    def session(self) -> sqlmodel.Session:
        return sqlmodel.Session(self.database_engine)
