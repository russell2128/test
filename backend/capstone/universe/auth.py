import datetime
import secrets
import copy
import dataclasses

from collections.abc import Mapping

import jwt
import passlib.context
import pydantic


@dataclasses.dataclass
class AuthenticationWand:
    algorithm: str = dataclasses.field(default="HS256")
    expire_period: datetime.timedelta = dataclasses.field(
        default=datetime.timedelta(hours=1)
    )
    secret_key: str = dataclasses.field(default_factory=lambda: secrets.token_hex(32))
    pwd_context: passlib.context.CryptContext = dataclasses.field(
        default_factory=lambda: passlib.context.CryptContext(
            schemes=["bcrypt"], deprecated="auto"
        )
    )

    def create_access_token(self, data: dict):
        to_encode = copy.deepcopy(data)
        expire = datetime.datetime.now(datetime.timezone.utc) + self.expire_period
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, plain_password: str) -> str:
        return self.pwd_context.hash(plain_password)
