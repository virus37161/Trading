from django.contrib import admin, messages
from .models import ContractTF, Signals, SettingsApp
from .services.services_admin import scan_signals
from datetime import datetime

class ContractTFAdmin(admin.ModelAdmin):
    list_display = ('contract', 'timeframe', 'send_to_telegram', 'take_profit_2', 'take_profit_1', 'stop_loss', 'signals_quantity')
    list_filter = ('contract', 'timeframe', 'send_to_telegram','signals_quantity')
    search_fields = ('contract__name', )
    actions = ['set_to_send', 'set_no_to_send', 'analitic']

    @admin.action(description="Установить отправку")
    def set_to_send(self, request, queryset):
        queryset.update(send_to_telegram=True)

    @admin.action(description="Отменить отправку")
    def set_no_to_send(self, request, queryset):
        queryset.update(send_to_telegram=False)

    @admin.action(description="Подсчет")
    def analitic(self, request, queryset):
        if SettingsApp.objects.get(id=1).scanning_signals:
            messages.add_message(request, messages.ERROR,"Ошибка, попробуйте позже. В настоящее время осуществляется сканирование!")
        elif 13 <= datetime.now().minute <= 15 or 28 <= datetime.now().minute <= 30 or 43 <= datetime.now().minute <= 45 or 58 <= datetime.now().minute <= 60:
            messages.add_message(request, messages.WARNING, "Скоро начнется сканирование, попробуйте позже.")
        else:
            for obj in queryset:
                obj.check_stop_loss()
                obj.check_take_profit_1()
                obj.check_take_profit_2()
                obj.check_signals_quantity()
            messages.add_message(request, messages.SUCCESS, "Подсчет прошел успешно!")

class SignalsAdmin(admin.ModelAdmin):
    list_display = ('contract', 'timeframe', 'long_or_short', 'entry_point', 'stop_loss',
                    'take_profit1', 'take_profit2', 'check_take_profit_1', 'check_take_profit_2', 'activity', 'tracking','bar_time')
    list_filter = ('contract', 'timeframe', 'check_take_profit_1', 'check_take_profit_2', 'activity', 'tracking', 'long_or_short')
    search_fields = ('contract__name',)
    actions = ['tracking']

    @admin.action(description='Отслеживание сигналов')
    def tracking(self, request, queryset):
        if SettingsApp.objects.get(id=1).scanning_signals:
            messages.add_message(request, messages.ERROR,"Ошибка, попробуйте позже. В настоящее время осуществляется сканирование!")
        elif 10 <= datetime.now().minute <= 15 or 25 <= datetime.now().minute <= 30 or 40 <= datetime.now().minute <= 45 or 55 <= datetime.now().minute <= 60:
            messages.add_message(request, messages.WARNING, "Скоро начнется сканирование, попробуйте позже.")
        else:
            scan_signals(queryset)
            messages.add_message(request, messages.SUCCESS, "Отслеживание сигналов прошло успешно!")


class SettingsAppAdmin(admin.ModelAdmin):
    list_display = ('quantity_signals_to_send',)

admin.site.register(ContractTF, ContractTFAdmin)
admin.site.register(Signals, SignalsAdmin)
admin.site.register(SettingsApp, SettingsAppAdmin)