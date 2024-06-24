import copy
import datetime
import secrets

import jwt
import passlib.context

import capstone._universe.wands


class AuthenticationWand(capstone._universe.wands.AbstractBaseWand):
    def __init__(
        self,
        central_hub_,
        *,
        algorithm: str = "HS256",
        expire_period: datetime.timedelta = None,
        secret_key: str = None,
        pwd_context: passlib.context.CryptContext = None
    ):
        super().__init__(central_hub_)
        self.__algorithm = algorithm
        self.__expire_period: datetime.timedelta = (
            expire_period
            if isinstance(expire_period, datetime.timedelta)
            else datetime.timedelta(hours=1)
        )
        self.__secret_key: str = (
            secret_key if isinstance(secret_key, str) else secrets.token_hex(32)
        )
        self.__pwd_context: passlib.context.CryptContext = (
            pwd_context
            if isinstance(pwd_context, passlib.context.CryptContext)
            else passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")
        )

    def create_access_token(self, data: dict):
        to_encode = copy.deepcopy(data)
        expire = datetime.datetime.now(datetime.timezone.utc) + self.__expire_period
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.__secret_key, algorithm=self.__algorithm
        )
        return encoded_jwt

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.__pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, plain_password: str) -> str:
        return self.__pwd_context.hash(plain_password)