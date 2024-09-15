from ..models import *
import time
from pybit.unified_trading import HTTP
from .base import *
from .signal_1 import tracking_signal, delete_last_singals
from datetime import datetime


def scan_signals(queryset):
    session = HTTP()
    data = now_time()
    for contract_obj in queryset:

        time_to_minus = time_that_need_minus(contract_obj, data)
        if (time_to_minus == None) or (contract_obj.activity == False and contract_obj.check_scan == False):
            continue
        s = session.get_kline(
            category="linear",
            symbol=contract_obj.contract.name,
            interval=contract_obj.timeframe.name,
            start=data.get('time') - time_to_minus.get('start'),
            end=data.get('time')-time_to_minus.get('end'),
            )

        if s.get('result').get('list')==[]:
            contract_obj.delete()
            continue

        tracking_signal(s, contract_obj)

        if contract_obj.activity == False:
            contract_obj.check_scan = True
            contract_obj.save()


def time_that_need_minus(contract_obj, data):
    dt_obj = datetime.strptime(f'{contract_obj.bar_time}', '%Y-%m-%d %H:%M:%S')
    dt_obj = dt_obj.timestamp()*1000
    start_end = data.get('time') - dt_obj
    if start_end == 0:
        return None
    if contract_obj.timeframe.name == 15:
        start_minus = start_end + 900000
        end_minus = 900000
    elif contract_obj.timeframe.name == 30:
        start_minus = 1800000 + start_end
        end_minus = 1800000
    elif contract_obj.timeframe.name == 60:
        start_minus = 3600000 + start_end
        end_minus = 3600000
    return {'start': start_minus, 'end': end_minus}

def tracking_signal(s, contract_obj):
    list_bars = s.get('result').get('list')
    signal = contract_obj
    if list_bars:
        for data in list_bars:
            if signal.check_take_profit_1 == False:
                if float(data[3]) <= signal.take_profit1 <= float(data[2]) and not float(data[3]) <= signal.stop_loss <= float(data[2]):
                    if float(data[3]) <= signal.take_profit2 <= float(data[2]):
                        signal.check_take_profit_2 = True
                        signal.activity = False
                        signal.save()
                        break
                        delete_last_singals(contract_obj)
                    elif signal.check_take_profit_1 == False:
                        signal.check_take_profit_1 = True
                        signal.save()
                elif float(data[3]) <= signal.take_profit1 <= float(data[2]):
                    low_tf = request_low_tf(signal.contract.name, signal.timeframe.name, data[0])
                    for bar in low_tf[::-1]:

                        if float(bar[3]) <= signal.take_profit1 <= float(bar[2]) and not float(bar[3]) <= signal.stop_loss <= float(bar[2]):
                            signal.check_take_profit_1 = True
                            signal.activity = False
                            signal.save()
                            break
                            delete_last_singals(contract_obj)
                        elif not float(bar[3]) <= signal.take_profit1 <= float(bar[2]) and float(bar[3]) <= signal.stop_loss <= float(bar[2]):
                            signal.activity = False
                            signal.save()
                            delete_last_singals(contract_obj)
                            break
                        else:
                            signal.tracking = False
                elif float(data[3]) <= signal.stop_loss <= float(data[2]) and not float(
                        data[3]) <= signal.take_profit1 <= float(data[2]):
                    signal.activity = False
                    signal.save()
                    break
                    delete_last_singals(contract_obj)
            else:
                if float(data[3]) <= signal.take_profit2 <= float(data[2]) and not float(data[3]) <= signal.stop_loss <= float(data[2]):
                    signal.check_take_profit_2 = True
                    signal.check_take_profit_1 = False
                    signal.activity = False
                    signal.save()
                    break
                    delete_last_singals(contract_obj)
                elif float(data[3]) <= signal.take_profit2 <= float(data[2]):
                    low_tf = request_low_tf(signal.contract.name, signal.timeframe.name, data[0])
                    for bar in low_tf[::-1]:
                        if float(bar[3]) <= signal.take_profit2 <= float(bar[2]) and not float(bar[3]) <= signal.stop_loss <= float(bar[2]):
                            signal.check_take_profit_2 = True
                            signal.check_take_profit_1 = False
                            signal.activity = False
                            signal.save()
                            delete_last_singals(contract_obj)
                            break
                        elif not float(bar[3]) <= signal.take_profit2 <= float(bar[2]) and float(bar[3]) <= signal.stop_loss <= float(bar[2]):
                            signal.activity = False
                            signal.save()
                            delete_last_singals(contract_obj)
                            break
                        else:
                            signal.tracking = False
                elif float(data[3]) <= signal.stop_loss <= float(data[2]) and not float(data[3]) <= signal.take_profit2 <= float(data[2]):
                    signal.activity = False
                    signal.save()
                    break
                    delete_last_singals(contract_obj)

def request_low_tf(contract, timeframe, time):
    session = HTTP()
    if timeframe == 15:
        interval = 3
        start_minus = 900000
    elif timeframe == 30:
        interval = 3
        start_minus = 1800000
    elif timeframe == 60:
        interval = 3
        start_minus = 3600000


    s = session.get_kline(
        category="linear",
        symbol=contract,
        interval=interval,
        start=int(time) - start_minus,
        end=int(time),
    )
    return s.get('result').get('list')