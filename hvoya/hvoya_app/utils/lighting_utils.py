# Этот модуль предназначен для работы с данными касающихся освещения

from datetime import datetime, timedelta

from .settings_utils import get_settings_data


def get_lighting_data() -> dict:
    """
     Отдает словарь со статусом работы лампы и временем до включения/отключения.
    """
    current_datetime = datetime.now()
    settings = get_settings_data()
    lamp_on_time = current_datetime.replace(hour=int(settings['lamp_on_time']), minute=0, second=0, microsecond=0)
    lamp_off_time = current_datetime.replace(hour=int(settings['lamp_off_time']), minute=0, second=0, microsecond=0)

    if lamp_on_time <= current_datetime <= lamp_off_time:
        lamp_on = True
        time_value = lamp_off_time - current_datetime

    else:
        lamp_on = False
        time_value = (
            lamp_on_time - current_datetime if
            current_datetime <= lamp_on_time else
            (lamp_on_time + timedelta(days=1)) - current_datetime
        )
    hour, residue = divmod(time_value.seconds, 3600)
    minute = residue // 60
    lighting_data = {
        'lamp_on': lamp_on,
        'time_value': '{}:{}'.format(correct_lamp_time(hour), correct_lamp_time(minute))
    }
    return lighting_data


def correct_lamp_time(time: int) -> str:
    """
    Добавляет '0' перед переданным значением времени, если оно состоит
    только из одного символа, приводя формат времни из '1:12' в '01:12'.
    """
    time_to_str = str(time)
    if len(time_to_str) < 2:
        return '{}{}'.format('0', time)
    return time_to_str
