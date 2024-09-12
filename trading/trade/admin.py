from django.contrib import admin
from .models import ContractTF, Signals, SettingsApp
from .services.services_admin import scan_signals

class ContractTFAdmin(admin.ModelAdmin):
    list_display = ('contract', 'timeframe', 'send_to_telegram', 'take_profit_2', 'take_profit_1', 'stop_loss')
    list_filter = ('contract', 'timeframe', 'send_to_telegram')
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
        for obj in queryset:
            obj.check_stop_loss()
            obj.check_take_profit_1()
            obj.check_take_profit_2()


class SignalsAdmin(admin.ModelAdmin):
    list_display = ('contract', 'timeframe', 'long_or_short', 'entry_point', 'stop_loss',
                    'take_profit1', 'take_profit2', 'check_take_profit_1', 'check_take_profit_2', 'activity', 'tracking','bar_time')
    list_filter = ('contract', 'timeframe', 'check_take_profit_1', 'check_take_profit_2', 'activity', 'tracking', 'long_or_short')
    search_fields = ('contract__name',)
    actions = ['tracking']

    @admin.action(description='Отслеживание сигналов')
    def tracking(self, request, queryset):
        scan_signals(queryset)

class SettingsAppAdmin(admin.ModelAdmin):
    list_display = ('quantity_signals_to_send',)

admin.site.register(ContractTF, ContractTFAdmin)
admin.site.register(Signals, SignalsAdmin)
admin.site.register(SettingsApp, SettingsAppAdmin)