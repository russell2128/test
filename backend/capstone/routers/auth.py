from typing import Annotated

import fastapi
import fastapi.routing
import fastapi.security
import pydantic

import capstone.data.dbtable
import capstone.data.type as cat
import capstone.universe
import capstone.utility.valid

router = fastapi.routing.APIRouter()

oauth2_scheme = fastapi.security.OAuth2PasswordBearer(tokenUrl="login")


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[fastapi.security.OAuth2PasswordRequestForm, fastapi.Depends()]
) -> Token:
    user = await capstone.universe.universal_wch.query_wand.lookup_user(
        form_data.username
    )
    if user is None:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username of password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not capstone.universe.universal_wch.authentication_wand.verify_password(
        form_data.password, user.hashed_passwd
    ):
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username of password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = (
        capstone.universe.universal_wch.authentication_wand.create_access_token(
            {"sub": user.username}
        )
    )

    return Token(access_token=access_token, token_type="bear")


@router.post("/register")
async def register_new_account(
    form_data: Annotated[fastapi.security.OAuth2PasswordRequestForm, fastapi.Depends()],
    fullname: str,
    email: str,
) -> cat.Result[Token]:
    if (
        await capstone.universe.universal_wch.query_wand.lookup_user(form_data.username)
        is not None
    ):
        return cat.Result[Token](
            status=cat.ResultVariant.ERROR,
            msg=f"Username {form_data.username} already exists.",
        )

    if not capstone.utility.valid.is_strong_password(form_data.password):
        return cat.Result[Token](
            status=cat.ResultVariant.ERROR,
            msg="Password is too weak",
        )

    if not capstone.utility.valid.is_valid_email(email):
        return cat.Result[Token](
            status=cat.ResultVariant.ERROR,
            msg="Invalid email address",
        )

    if await capstone.universe.universal_wch.query_wand.is_email_already_taken(email):
        return cat.Result[Token](
            status=cat.ResultVariant.ERROR,
            msg=f"Email address {email} has already been registered for other accounts.",
        )

    new_user = capstone.data.dbtable.User(
        username=form_data.username,
        email=email,
        fullname=fullname,
        hashed_passwd=capstone.universe.universal_wch.authentication_wand.hash_password(
            form_data.password
        ),
    )
    capstone.universe.universal_wch.database_engine_wand.insert_item(new_user)

    access_token = (
        capstone.universe.universal_wch.authentication_wand.create_access_token(
            {"sub": new_user.username}
        )
    )

    return cat.Result[Token](
        status=capstone.data.type.ResultVariant.OK, content=access_token
    )