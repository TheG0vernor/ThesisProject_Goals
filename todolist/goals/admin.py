from django.contrib import admin

from goals.models import GoalsCategory, Goals, GoalsComments, Board

# Register your models here.
admin.site.register(GoalsCategory)
admin.site.register(Goals)
admin.site.register(GoalsComments)
admin.site.register(Board)
