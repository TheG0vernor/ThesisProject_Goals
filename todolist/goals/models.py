from enum import Enum

from django.core.validators import MinLengthValidator
from django.db import models

from core.models import User


class DatesModelMixin(models.Model):
    """Абстрактный класс для наследования повторяющихся полей в другими классами"""
    class Meta:
        abstract = True
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")
    # другой вариант автоматического проставления DateTime:
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.created = timezone.now()  # если объект только создан - проставляем DateTime
    #     self.updated = timezone.now()  # DateTime обновления проставляем всегда
    #     return super().save(*args, **kwargs)


class StatusGoal(Enum):
    """Статусы целей"""
    to_do = (1, "К выполнению")
    in_progress = (2, "В процессе")
    done = (3, "Выполнено")
    archived = (4, "Архив")


class PriorityGoal(Enum):  # также можно наследоваться от IntegerChoices. Тогда в аттрибуте choices поля модели указать Classname.choices. Убрать кортежи.
    """Приоритеты целей"""
    low = (1, "Низкий")
    medium = (2, "Средний")
    high = (3, "Высокий")
    critical = (4, "Критический")


class Board(DatesModelMixin):
    """Модель доски"""
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(max_length=255, validators=[MinLengthValidator(limit_value=1)], verbose_name="Название")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалена")


class BoardParticipant(DatesModelMixin):
    """Модель участника доски"""
    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
        unique_together = ['user', 'board']  # проверка, что поля user и board уникальны в паре друг с другом

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    role = models.PositiveSmallIntegerField(
        choices=Role.choices, verbose_name="Роль", default=Role.owner)
    user = models.ForeignKey(to=User, verbose_name="Пользователь", related_name='participants', on_delete=models.PROTECT)
    board = models.ForeignKey(to=Board, verbose_name="Доска", related_name='participants', on_delete=models.PROTECT)


class GoalsCategory(DatesModelMixin):
    """Категория целей"""
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    user = models.ForeignKey(to=User, verbose_name="Автор", on_delete=models.PROTECT)
    board = models.ForeignKey(to=Board, verbose_name="Доска", related_name='categories', on_delete=models.PROTECT)


class Goals(DatesModelMixin):
    """Модель целей"""
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    title = models.CharField(verbose_name="Заголовок", validators=[MinLengthValidator(limit_value=1)], max_length=255)
    description = models.CharField(verbose_name="Описание", null=True, blank=True, max_length=1000)  # также может быть TextField, без max_length
    due_date = models.DateField(verbose_name="Дата выполнения", null=True, blank=True)
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


class GoalsComments(DatesModelMixin):
    """Комментарии целей"""
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    text = models.CharField(max_length=500, validators=[MinLengthValidator(limit_value=1)])
    user = models.ForeignKey(to=User, verbose_name="Автор", on_delete=models.PROTECT)
    goal = models.ForeignKey(to=Goals, verbose_name="Цель", on_delete=models.CASCADE)
