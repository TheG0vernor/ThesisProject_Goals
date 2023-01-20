import os

from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class BotVerificationView(UpdateAPIView):
    model = TgUser
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        data = self.serializer_class(request.data).data
        tg_client = TgClient(token=os.environ.get('TG_BOT_API_TOKEN'))
        tg_user = TgUser.objects.filter(verification_code=data['verification_code']).first()
        if not tg_user:
            return Response(status=HTTP_400_BAD_REQUEST)
        tg_user.user = request.user
        tg_user.save()

        tg_client.send_message(chat_id=tg_user.telegram_chat_id, text='Успешно отправлено')
        return Response(data=data, status=HTTP_201_CREATED)
