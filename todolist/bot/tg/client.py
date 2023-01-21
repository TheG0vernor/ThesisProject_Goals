import requests
from rest_framework import schemas

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    """Обращения к телеграмному боту"""
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        # try:
        url = self.get_url(method='getUpdates')
        response = requests.get(url=url, params={"offset": offset, "timeout": timeout})
        return GetUpdatesResponse(**response.json())
        # return GET_UPDATES_SCHEMA.load(data=response.json())
        # except Exception as e:
        #     raise NotImplementedError(e)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        try:
            url = self.get_url(method='sendMessage')
            response = requests.get(url=url, params={"chat_id": chat_id, "text": text})
            # return SEND_MESSAGE_RESPONSE_SCHEMA.load(data=response.json())
            return SendMessageResponse(**response.json())
        except Exception as e:
            raise NotImplementedError(e)
