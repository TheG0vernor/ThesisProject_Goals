import os

from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message


class Command(BaseCommand):
    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient(token=os.environ.get('TG_BOT_API_TOKEN'))
        while True:
            res = tg_client.get_updates(offset=offset, timeout=3)
            for item in res.result:
                offset = item.update_id + 1
                if hasattr(__obj=item, __name='message'):  # если объект имеет атрибут с заданным именем
                    print(item.message)
                    # self.handle_message(item.message)

    # tg_client = TgClient(token=os.environ.get('TG_BOT_API_TOKEN'))
    #
    # def handle_message(self, message: Message):
    #     telegram_user, created = TgUser.objects.get_or_create(
    #         telegram_user_id=message.msg_from.id,
    #         telegram_chat_id=message.chat.id,
    #     )
    #     if created:
    #         telegram_user.generate_verification_code()
    #         self.tg_client.send_message(
    #             chat_id=message.chat.id,
    #             text=f'Подтвердите, пожалуйста, свой аккаунт'
    #                  f'Для подтверждения нужно ввести код {telegram_user.verification_code} на сайте.'
    #         )
    #     if message.text == '/goals':
    #         self.get_goals(message, telegram_user)
    #     elif message.text == '/create':
    #         pass
