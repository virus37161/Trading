# Generated by Django 5.0.7 on 2024-08-30 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0006_alter_signals_check_take_profit_1'),
    ]

    operations = [
        migrations.AddField(
            model_name='signals',
            name='bar_time',
            field=models.TextField(default=None, verbose_name='Бар'),
            preserve_default=False,
        ),
    ]
