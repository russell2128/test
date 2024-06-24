import sqlmodel


class User(sqlmodel.SQLModel, table=True):
    username: str = sqlmodel.Field(primary_key=True, nullable=False)
    email: str
    fullname: str
    hashed_passwd: str