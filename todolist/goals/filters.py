import django_filters
from django.db import models
from django_filters import rest_framework

from goals.models import Goals


class GoalsFilter(rest_framework.FilterSet):
    """Фильтры для целей"""
    class Meta:
        model = Goals
        fields = {
            "due_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            "priority": ("exact", "in"),
        }
        filter_overrides = {
            models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter}
        }
