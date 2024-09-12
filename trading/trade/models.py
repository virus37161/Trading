from django.db import models
from computedfields.models import ComputedFieldsModel, computed, compute


class TimeFrame(models.Model):
    name = models.IntegerField(verbose_name='ТФ')

    def __str__(self):
        return f'{self.name}'


class Contracts(models.Model):
    name = models.TextField(verbose_name="Контракт")

    def __str__(self):
        return f'{self.name}'


class ContractTF(models.Model):
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE, verbose_name="Контракт")
    timeframe = models.ForeignKey(TimeFrame, on_delete=models.CASCADE, verbose_name="ТФ")
    send_to_telegram = models.BooleanField(default=False, verbose_name="Отправка")
    stop_loss = models.IntegerField(default=0,verbose_name="CЛ в %")
    take_profit_1 = models.IntegerField(default=0, verbose_name="ТП1 в %")
    take_profit_2 = models.IntegerField(default=0, verbose_name="ТП2 в %")

    def check_stop_loss(self):
        if len(self.signals_set.all())== 0:
            self.stop_loss = 0
            self.save()
        else:
            self.stop_loss = int((len(self.signals_set.all().filter(activity=False, check_take_profit_1=False, check_take_profit_2=False)) / len(self.signals_set.all())) * 100)
            self.save()

    def check_take_profit_1(self):
        if len(self.signals_set.all()) == 0:
            self.take_profit_1 = 0
            self.save()
        else:
            self.take_profit_1 = int((len(self.signals_set.all().filter(activity=False, check_take_profit_1=True,
                                                                    check_take_profit_2=False)) / len(
                self.signals_set.all())) * 100)
            self.save()

    def check_take_profit_2(self):
        if len(self.signals_set.all()) == 0:
            self.take_profit_2 = 0
            self.save()
        else:
            self.take_profit_2 = int((len(self.signals_set.all().filter(activity=False, check_take_profit_1=False,
                                                                    check_take_profit_2=True)) / len(
                self.signals_set.all())) * 100)
            self.save()

    class Meta:
        verbose_name_plural = "Контракты"
        verbose_name = "Контракт"


class Signals(models.Model):
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE, verbose_name="Контракт")
    timeframe = models.ForeignKey(TimeFrame, on_delete=models.CASCADE, verbose_name="ТФ")
    long_or_short = models.TextField(blank=False, verbose_name="Направление")
    entry_point = models.FloatField(blank=False, verbose_name="ТВ")
    stop_loss = models.FloatField(blank=False, verbose_name="СЛ")
    take_profit1 = models.FloatField(blank=False, verbose_name="ТП1")
    take_profit2 = models.FloatField(blank=False, verbose_name="ТП2")
    check_take_profit_1 = models.BooleanField(blank=True, default=False, verbose_name="Взятие ТП1")
    check_take_profit_2 = models.BooleanField(blank=True, default=False, verbose_name="Взятие ТП2")
    activity = models.BooleanField(blank=True, default=True, verbose_name="Активность")
    bar_time = models.TextField(verbose_name="Бар")
    tracking = models.BooleanField(blank=True, default=True, verbose_name="Отслеживание")
    contractTF = models.ForeignKey(ContractTF, on_delete=models.CASCADE)
    some_data = models.DateField(auto_now_add=True)
    some_time = models.TimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Сигналы"
        verbose_name = "Сигнал"

class SettingsApp(models.Model):
    quantity_signals_to_send = models.IntegerField(verbose_name="Количество для отправки")

    class Meta:
        verbose_name_plural = "Настройки"
        verbose_name = "Настройки"
