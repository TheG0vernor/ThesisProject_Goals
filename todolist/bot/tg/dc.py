from dataclasses import dataclass, field
from typing import List, Optional, ClassVar, Type

from marshmallow import EXCLUDE, Schema


@dataclass
class ChatMessageResponse:
    id: int
    first_name: Optional
    last_name: Optional
    username: Optional
    title: Optional
    type: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class FromMessageResponse:
    id: int
    is_bot: bool
    first_name: str | None
    last_name: str | None
    username: str | None
    language_code: str | None

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    message_id: int
    msg_from: FromMessageResponse = field(metadata={'data_key': 'from'})  # обращение будет происходить через поле from
    chat: ChatMessageResponse
    date: int
    text: Optional  # то же, что str | None

    class Meta:
        unknown = EXCLUDE  # неизвестные поля, которые не указаны в классе, игнорируются


@dataclass
class UpdateObj:
    update_id: int
    message: Message  # может быть импортирован из aiogram.types

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]  # Update может быть импортирован из aiogram.types (библиотека aiogram==2.24, не тестировалось)

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message  # Message может быть импортирован из aiogram.types (библиотека aiogram==2.24). В данном коде он создан вручную.

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE
