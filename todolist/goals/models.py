from django.db import models
from django.utils import timezone

from core.models import User


class GoalsCategory(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")
    user = models.ForeignKey(to=User, verbose_name="Автор", on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()  # если объект только создан - проставляем DateTime
        self.updated = timezone.now()  # DateTime обновления проставляем всегда
        return super().save(*args, **kwargs)
