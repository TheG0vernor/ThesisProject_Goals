import os
from datetime import datetime

from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goals, StatusGoal, GoalsCategory


class TgBotCondition:
    """Регламентирует состояния бота"""
    DEFAULT = 0
    CATEGORY_CHOICE = 1  # категория выбрана
    GOAL_CREATE = 2  # цель создана

    def __init__(self, condition=DEFAULT, category_id=None):
        self.condition = condition
        self.category_id = category_id

    def set_condition(self, condition):
        self.condition = condition

    def set_category_id(self, category_id):
        self.category_id = category_id


BOT_CONDITION = TgBotCondition()  # хранит текущее состояние бота


class Command(BaseCommand):
    help = 'Run Telegram bot'
    tg_client = TgClient(token=os.environ.get('TG_BOT_API_TOKEN'))

    def choice_category(self, message: Message, telegram_user: TgUser):
        categories = GoalsCategory.objects.filter(
            board__participants__user=telegram_user.user,
            is_deleted=False)
        categories_str = '\n'.join(['* ' + category.title for category in categories])

        self.tg_client.send_message(
            chat_id=message.chat.id,
            text=f"Выберите категорию: \n{categories_str}")

        BOT_CONDITION.set_condition(TgBotCondition.CATEGORY_CHOICE)

    def check_category(self, message):
        category = GoalsCategory.objects.filter(title=message.text)
        if category:
            self.tg_client.send_message(
                chat_id=message.chat.id,
                text=f'Введите заголовок цели')

            BOT_CONDITION.set_category_id(category_id=category.id)
            BOT_CONDITION.set_condition(condition=TgBotCondition.GOAL_CREATE)
        else:
            self.tg_client.send_message(
                chat_id=message.chat.id,
                text=f'Категория "{message.text}" отсутствует на Вашей доске')

    def create_goal(self, message, telegram_user):
        category = GoalsCategory.objects.get(pk=BOT_CONDITION.category_id)
        goal = Goals.objects.create(
            title=message.text,
            user=telegram_user.user,
            category=category,
        )
        self.tg_client.send_message(
            chat_id=message.chat.id,
            text=f'Цель {goal.title} успешно создана'
        )
        BOT_CONDITION.set_condition(TgBotCondition.DEFAULT)

    def get_goals(self, message, telegram_user):
        goals = Goals.objects.filter(
            category__board__participants__user=telegram_user.user
        ).exclude(status=StatusGoal.archived.value[0])
        goals_str = '\n'.join([goal.title for goal in goals])

        self.tg_client.send_message(
            chat_id=message.chat.id,
            text=f"Список Ваших целей: \n{goals_str}"
        )

    def cancel_operation(self, message):
        BOT_CONDITION.set_condition(TgBotCondition.DEFAULT)
        self.tg_client.send_message(
            chat_id=message.chat.id,
            text='Операция отменена'
        )

    def handle_message(self, message: Message):
        telegram_user, created = TgUser.objects.get_or_create(
            telegram_user_id=message.msg_from.id,
            telegram_chat_id=message.chat.id,
        )
        if created:
            telegram_user.generate_verification_code()
            self.tg_client.send_message(
                chat_id=message.chat.id,
                text=f'Подтвердите, пожалуйста, свой аккаунт:\n'
                     f'Для подтверждения нужно ввести код {telegram_user.verification_code} на сайте.'
            )
        if message.text == '/goals':
            self.get_goals(message, telegram_user)
        elif message.text == '/create':
            self.choice_category(message, telegram_user)
        elif message.text == '/cancel':
            self.cancel_operation(message)
        elif BOT_CONDITION.condition == TgBotCondition.CATEGORY_CHOICE:
            self.check_category(message)
        elif BOT_CONDITION.condition == TgBotCondition.GOAL_CREATE:
            self.create_goal(message, telegram_user)
        else:
            self.tg_client.send_message(
                chat_id=message.chat.id,
                text=f"Команда неизвестна: {message.text}")

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient(token=os.environ.get('TG_BOT_API_TOKEN'))
        while True:
            res = tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                if hasattr(item, 'message'):  # если объект имеет атрибут с заданным именем
                    self.handle_message(item.message)


