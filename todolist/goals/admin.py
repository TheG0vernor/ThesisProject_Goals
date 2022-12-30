from django.contrib import admin

from goals.models import GoalsCategory, Goals

# Register your models here.
admin.site.register(GoalsCategory)
admin.site.register(Goals)
