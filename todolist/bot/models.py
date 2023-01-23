from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.crypto import get_random_string

from core.models import User


class TgUser(models.Model):
    """Модель пользователя телеграм, который взаимодействует с ботом"""
    telegram_chat_id = models.PositiveBigIntegerField()
    telegram_user_id = models.PositiveBigIntegerField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    telegram_username = models.CharField(max_length=32, validators=[MinLengthValidator(5)])
    verification_code = models.CharField(max_length=10, unique=True)

    def generate_verification_code(self) -> str:
        new_code = get_random_string(length=10)
        self.verification_code = new_code
        self.save()
        return new_code
