from django.core.management.base import BaseCommand

from bot.tg.client import TgClient


class Command(BaseCommand):

    def handle_message(self, message):
        pass

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient("token")
        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                print(item.message)
                # if hasattr(__obj=item, __name='message'):  # если объект имеет атрибут с заданным именем
                #     # self.handle_message(item.message)
