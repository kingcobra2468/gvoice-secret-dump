from pydantic import BaseModel


class Cookie(BaseModel):
    domain: str = ""
    expiry: int | None = 0
    httpOnly: bool | None = False
    name: str | None = None
    path: str | None = None
    sameSite: str | None = None
    secure: bool | None = False
    value: str | None = None
