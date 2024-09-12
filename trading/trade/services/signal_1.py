from ..models import *
import time
from pybit.unified_trading import HTTP
from .base import *


def scan_signals():
    time_before = time.time()
    list_need_to_send = ContractTF.objects.filter(send_to_telegram=True).order_by("-take_profit_2", "-take_profit_1")
    quantity = SettingsApp.objects.get(id=1).quantity_signals_to_send
    list_need_to_send = list_need_to_send[:quantity:]
    session = HTTP()
    data = now_time()
    for contract_obj in ContractTF.objects.order_by('-send_to_telegram'):
        if contract_obj.timeframe.name in data.get('time_frame'):
            time_to_minus = time_that_need_minus(contract_obj.timeframe.name)
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
            send_and_save_signal(s, contract_obj, data, list_need_to_send)

    time_after = time.time()
    print(time_after - time_before)


def send_and_save_signal(s, contract_obj, data, list_need_to_send):
    result = check_of_size(s)
    if result.get('signal'):
        Signals.objects.create(entry_point=result.get('entry_point'),
                               stop_loss=result.get('stop_loss'),
                               take_profit1=result.get('take_profit_1'),
                               take_profit2=result.get('take_profit_2'),
                               contract_id=contract_obj.contract_id,
                               timeframe_id=contract_obj.timeframe_id,
                               bar_time=str(data.get('bar')),
                               long_or_short=result.get('long_or_short'),
                               contractTF_id=contract_obj.id
                            )
        if contract_obj in list_need_to_send:
            print (contract_obj.contract, contract_obj.timeframe)


def tracking_signal(s, contract_obj):
    data = s.get('result').get('list')
    signals_list = Signals.objects.filter(contract_id=contract_obj.contract_id, timeframe_id=contract_obj.timeframe_id, activity = True)
    if signals_list:
        for signal in signals_list:
            if signal.check_take_profit_1 == False:
                if float(data[0][3]) <= signal.take_profit1 <= float(data[0][2]) and not float(data[0][3]) <= signal.stop_loss <= float(data[0][2]):
                    if float(data[0][3]) <= signal.take_profit2 <= float(data[0][2]):
                        signal.check_take_profit_2 = True
                        signal.activity = False
                        signal.save()
                        delete_last_singals(contract_obj)
                    elif signal.check_take_profit_1 == False:
                        signal.check_take_profit_1 = True
                        signal.save()
                elif float(data[0][3]) <= signal.take_profit1 <= float(data[0][2]):
                    low_tf = request_low_tf(signal.contract.name, signal.timeframe.name)
                    for bar in low_tf[::-1]:
                        if float(bar[3]) <= signal.take_profit1 <= float(bar[2]) and not float(bar[3]) <= signal.stop_loss <= float(bar[2]):
                            signal.check_take_profit_1 = True
                            signal.activity = False
                            signal.save()
                            delete_last_singals(contract_obj)
                        elif not float(bar[3]) <= signal.take_profit1 <= float(bar[2]) and float(bar[3]) <= signal.stop_loss <= float(bar[2]):
                            signal.activity = False
                            signal.save()
                            delete_last_singals(contract_obj)
                            break
                        else:
                            signal.tracking = False
                elif float(data[0][3]) <= signal.stop_loss <= float(data[0][2]) and not float(
                        data[0][3]) <= signal.take_profit1 <= float(data[0][2]):
                    signal.activity = False
                    signal.save()
                    delete_last_singals(contract_obj)
            else:
                if float(data[0][3]) <= signal.take_profit2 <= float(data[0][2]) and not float(data[0][3]) <= signal.stop_loss <= float(data[0][2]):
                    signal.check_take_profit_2 = True
                    signal.check_take_profit_1 = False
                    signal.activity = False
                    signal.save()
                    delete_last_singals(contract_obj)
                elif float(data[0][3]) <= signal.take_profit2 <= float(data[0][2]):
                    low_tf = request_low_tf(signal.contract.name, signal.timeframe.name)
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
                elif float(data[0][3]) <= signal.stop_loss <= float(data[0][2]) and not float(data[0][3]) <= signal.take_profit2 <= float(data[0][2]):
                    signal.activity = False
                    signal.save()
                    delete_last_singals(contract_obj)

def request_low_tf(contract, timeframe):
    session = HTTP()
    data = now_time()
    if timeframe == 15:
        interval = 3
        start_minus = 1800000
        end_minus = 900000
    elif timeframe == 30:
        interval = 3
        start_minus = 3600000
        end_minus = 1800000
    elif timeframe == 60:
        interval = 3
        start_minus = 7200000
        end_minus = 3600000

    s = session.get_kline(
        category="linear",
        symbol=contract,
        interval=interval,
        start=data.get('time') - start_minus,
        end=data.get('time') - end_minus,
    )
    return s.get('result').get('list')




def check_of_size(s):
    data = s.get('result').get('list')
    if check_of_green_and_red(data):
        bar1 = abs(float(data[0][1])-float(data[0][4]))
        bar2 = abs(float(data[1][1])-float(data[1][4]))
        bar3 = abs(float(data[2][1])-float(data[2][4]))
        if bar3 * 0.51 <= bar2 < bar3 * 0.98 and bar2 * 1.02 < bar1:
            digits = len(data[0][1]) - len(str(int(float(data[0][1])))) - 1
            if (float(data[0][1])-float(data[0][4])) > 0:
                long_or_short = "Short"
                entry_point = round(float(data[0][4]), digits)
                stop_loss = round((float(data[0][2]) + ((float(data[0][2])-entry_point)*0.01)), digits)
                take_profit_1 = round((entry_point - (stop_loss - entry_point)), digits)
                take_profit_2 = round((entry_point - ((stop_loss - entry_point) * 2)), digits)
            else:
                long_or_short = "Long"
                entry_point = round((float(data[0][4])), digits)
                stop_loss = round((float(data[0][3]) - ((entry_point-float(data[0][3]))*0.01)), digits)
                take_profit_1 = round((entry_point + (entry_point - stop_loss)),digits)
                take_profit_2 = round((entry_point + ((entry_point - stop_loss) * 2)), digits)
            return {"signal": True, "long_or_short": long_or_short, "entry_point": entry_point, "stop_loss": stop_loss,
                    "take_profit_1": take_profit_1, "take_profit_2": take_profit_2}
        else:
            return {"signal": False}
    else:
        return {"signal": False}

def check_of_green_and_red(data):
    if (data[0][1] > data[0][4] and data[1][1] < data[1][4] and data[2][1] > data[2][4]) or \
        (data[0][1] < data[0][4] and data[1][1] > data[1][4] and data[2][1] < data[2][4]):
        return True
    else:
        return False

def time_that_need_minus(data):
    if data == 15:
        start_minus = 2700000
        end_minus = 900000
    elif data == 30:
        start_minus = 5400000
        end_minus = 1800000
    elif data == 45:
        start_minus = 8100000
        end_minus = 2700000
    elif data == 60:
        start_minus = 10800000
        end_minus = 3600000
    return {'start': start_minus, 'end': end_minus}

def delete_last_singals(contract_obj):
    list_of_signals = (
        Signals.objects.filter(contract_id=contract_obj.contract_id, timeframe_id=contract_obj.timeframe_id,
                               activity=False).
        order_by("some_data", "some_time"))
    if len(list_of_signals) > 20:
        list_of_signals[0].delete()
        print(
            f"Удаление: {contract_obj.contract}:{contract_obj.timeframe}:{contract_obj.some_data}:{contract_obj.some_time}")



