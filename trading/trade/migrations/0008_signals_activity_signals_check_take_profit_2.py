# Generated by Django 5.0.7 on 2024-08-31 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0007_signals_bar_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='signals',
            name='activity',
            field=models.BooleanField(blank=True, default=True, verbose_name='Активность'),
        ),
        migrations.AddField(
            model_name='signals',
            name='check_take_profit_2',
            field=models.BooleanField(blank=True, default=False, verbose_name='Взятие ТП2'),
        ),
    ]
