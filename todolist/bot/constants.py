import marshmallow_dataclass

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse

# константы схем dataclasses
GET_UPDATES_SCHEMA = marshmallow_dataclass.class_schema(GetUpdatesResponse)()
SEND_MESSAGE_RESPONSE_SCHEMA = marshmallow_dataclass.class_schema(SendMessageResponse)()
