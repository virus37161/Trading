from datetime import datetime

def now_time():
    now = datetime.now().minute
    if 0 <= now < 15:
        minute = 0
        time_frame = [15, 30, 60]
    elif 15 <= now < 30:
        minute = 15
        time_frame = [15]
    elif 30 <= now < 45:
        minute = 30
        time_frame = [15, 30]
    elif 45 <= now < 60:
        minute = 45
        time_frame = [15]
    data = datetime.now()
    data = data.replace(minute=minute, second=0, microsecond=0)
    dt_obj = datetime.strptime(f'{data}', '%Y-%m-%d %H:%M:%S')
    dt_obj = dt_obj.timestamp()*1000
    return {'time': dt_obj, 'time_frame': time_frame, 'bar': data}