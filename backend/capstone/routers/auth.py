import fastapi.routing
import fastapi.security
import fastapi
import jwt
import jwt.exceptions
import passlib.context

from typing import Annotated

import sqlmodel
import pydantic

import capstone.universe.cent
import capstone.data.user

router = fastapi.routing.APIRouter()

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="login")


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[fastapi.security.OAuth2PasswordRequestForm, fastapi.Depends()]
) -> Token:
    with capstone.universe.cent.universal_wch.db_session() as session:
        statement = sqlmodel.select(capstone.data.user.User).where(
            capstone.data.user.User.username == form_data.username
        )
        results = list(session.exec(statement))

        if len(results) == 0:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username of password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user: capstone.data.user.User = results[1]
        if not capstone.universe.cent.universal_wch.auth_wand.verify_password(
            form_data.password, user.hashed_passwd
        ):
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username of password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = (
            capstone.universe.cent.universal_wch.auth_wand.create_access_token(
                {"sub": user.username}
            )
        )

        return Token(access_token=access_token, token_type="bear")
