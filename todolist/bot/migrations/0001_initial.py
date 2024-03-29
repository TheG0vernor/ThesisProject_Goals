# Generated by Django 4.1.3 on 2023-01-20 11:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_chat_id', models.PositiveIntegerField()),
                ('telegram_user_id', models.PositiveIntegerField()),
                ('telegram_username', models.CharField(max_length=32, validators=[django.core.validators.MinLengthValidator(5)])),
                ('verification_code', models.CharField(max_length=10, unique=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
