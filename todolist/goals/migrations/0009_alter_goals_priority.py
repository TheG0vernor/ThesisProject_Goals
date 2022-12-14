# Generated by Django 4.1.3 on 2023-01-09 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0008_alter_goals_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goals',
            name='priority',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Низкий'), (2, 'Средний'), (3, 'Высокий'), (4, 'Критический')], default=2, verbose_name='Приоритет'),
        ),
    ]
