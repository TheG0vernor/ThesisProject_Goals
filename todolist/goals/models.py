from enum import Enum

from django.core import validators
from django.db import models
from django.utils import timezone

from core.models import User


class StatusGoal(Enum):
    to_do = (1, "К выполнению")
    in_progress = (2, "В процессе")
    done = (3, "Выполнено")
    archived = (4, "Архив")


class PriorityGoal(Enum):  # также можно наследоваться от IntegerChoices. Тогда в аттрибуте choices поля модели указать Classname.choices. Убрать кортежи.
    low = (1, "Низкий")
    medium = (2, "Средний")
    high = (3, "Высокий")
    critical = (4, "Критический")


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


class Goals(models.Model):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    title = models.CharField(verbose_name="Заголовок", validators=[validators.MinLengthValidator(limit_value=1)], max_length=255)
    description = models.CharField(verbose_name="Описание", null=True, blank=True, max_length=1000)  # также может быть TextField, без max_length
    due_date = models.DateField(verbose_name="Дата выполнения", null=True, blank=True)
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус",
        choices=[status.value for status in StatusGoal],
        default=StatusGoal.to_do.value[0])
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет",
        choices=[priority.value for priority in PriorityGoal],
        default=PriorityGoal.medium.value[0])
    user = models.ForeignKey(verbose_name="Автор", to=User, on_delete=models.PROTECT)  # также можно указать модель способом to="core.User"
    category = models.ForeignKey(verbose_name="Категория", to=GoalsCategory, on_delete=models.CASCADE)  # когда category будет удалена, goals тоже удалятся из базы


class GoalsComments(models.Model):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    text = models.CharField(max_length=500, validators=[validators.MinLengthValidator(limit_value=1)])
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)
    user = models.ForeignKey(to=User, verbose_name="Автор", on_delete=models.PROTECT)
    goal = models.ForeignKey(to=Goals, verbose_name="Цель", on_delete=models.CASCADE)
