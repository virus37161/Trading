# Generated by Django 5.0.7 on 2024-08-31 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0009_signals_tracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='signals',
            name='long_or_short',
            field=models.TextField(default=None, verbose_name='Направление'),
            preserve_default=False,
        ),
    ]
