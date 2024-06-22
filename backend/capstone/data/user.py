import uuid

import sqlmodel


class User(sqlmodel.SQLModel, table=True):
    username: str = sqlmodel.Field(primary_key=True, nullable=False)
    email: str | None = None
    fullname: str
    disabled: bool = False
    hashed_passwd: str
