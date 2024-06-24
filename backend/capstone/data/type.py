from typing import TypeVar, Generic

import pydantic
import enum

ContentT = TypeVar("ContentT")


class ResultVariant(enum.StrEnum):
    OK = "OK"
    ERROR = "ERROR"


class _PreResult(pydantic.BaseModel):
    status: ResultVariant = ResultVariant.OK
    msg: str = ""


class Result(_PreResult, Generic[ContentT]):
    content: ContentT | None = None