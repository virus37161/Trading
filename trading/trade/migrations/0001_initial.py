# Generated by Django 5.1 on 2024-08-29 09:36

import computedfields.resolver
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Контракт')),
            ],
        ),
        migrations.CreateModel(
            name='TimeFrame',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(verbose_name='ТФ')),
            ],
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop_loss', models.IntegerField(verbose_name='СЛ')),
                ('take_profit1', models.IntegerField(verbose_name='ТП1')),
                ('take_profit2', models.IntegerField(verbose_name='ТП2')),
                ('prosent_tp1', models.CharField(editable=False, max_length=20)),
                ('prosent_tp2', models.CharField(editable=False, max_length=20)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.contracts', verbose_name='Контракт')),
                ('timeframe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.timeframe', verbose_name='ТФ')),
            ],
            options={
                'abstract': False,
            },
            bases=(computedfields.resolver._ComputedFieldsModelBase, models.Model),
        ),
        migrations.CreateModel(
            name='Signals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_point', models.IntegerField(verbose_name='ТВ')),
                ('stop_loss', models.IntegerField(verbose_name='СЛ')),
                ('take_profit1', models.IntegerField(verbose_name='ТП1')),
                ('take_profit2', models.IntegerField(verbose_name='ТП2')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.contracts', verbose_name='Контракт')),
                ('timeframe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.timeframe', verbose_name='ТФ')),
            ],
        ),
        migrations.CreateModel(
            name='ContractTF',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_to_telegram', models.BooleanField(default=False)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.contracts', verbose_name='Контракт')),
                ('timeframe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trade.timeframe', verbose_name='ТФ')),
            ],
        ),
    ]
