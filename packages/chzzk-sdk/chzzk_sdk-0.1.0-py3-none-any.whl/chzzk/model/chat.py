from __future__ import annotations

from datetime import datetime
from typing import Optional, Any, Literal, TypeVar, Generic, Annotated

from pydantic import AfterValidator, Field

from chzzk.model import DefaultModel
from chzzk.utils import to_kst

T = TypeVar("T", bound="MessageBody")


class TemporaryRestrict(DefaultModel):
    temporary_restrict: bool
    times: int
    duration: Optional[Any] = None
    createdTime: Optional[Any] = None


class Token(DefaultModel):
    access_token: str
    temporary_restrict: TemporaryRestrict
    real_name_auth: bool
    extra_token: str


class MessageBody(DefaultModel):
    pass


class Connect(MessageBody):
    acc_tkn: str
    auth: Literal["SEND", "READ"]
    dev_type: int
    uid: str


class DefaultMessage(DefaultModel):
    cid: str = None
    svcid: Literal["game"] = "game"
    ver: str = None


class Message(DefaultMessage, Generic[T]):
    bdy: T
    cmd: int
    tid: int


class Blind(DefaultModel):
    service_id: str
    message_time: Optional[Annotated[datetime, AfterValidator(to_kst)]] = Field(alias="messageTime", default=None)
    blind_type: str
    blind_user_id: Optional[str]
    user_id: str
    message: Optional[str]
