# Generated by Django 4.1.3 on 2023-01-09 04:04

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0004_goals_user_alter_goals_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goals',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goals.goalscategory', verbose_name='Категория'),
        ),
        migrations.CreateModel(
            name='GoalsComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, validators=[django.core.validators.MinLengthValidator(limit_value=1)])),
                ('created', models.DateTimeField(verbose_name='Дата создания')),
                ('updated', models.DateTimeField(verbose_name='Дата последнего обновления')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goals.goals', verbose_name='Цель')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
    ]