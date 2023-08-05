from typing import Any, TypedDict


class RequestValidationError(TypedDict):
    loc: list[str]
    msg: str
    type: str


class ConflictError(TypedDict):
    loc: list[str]
    type: str
    msg: str
    info: dict[str, Any]


class UnauthorizedError(TypedDict):
    loc: list[str]
    type: str
    msg: str


class NotFoundError(TypedDict):
    loc: list[str]
    type: str
    msg: str
    info: dict[str, Any]


class HTTPErrorDetails(TypedDict):
    detail: list[
        RequestValidationError | ConflictError | UnauthorizedError | NotFoundError
    ]
