from django.db import models


class GrowBoxSettings(models.Model):
    minimal_soil_humidity = models.IntegerField('Минимальная влажность грунта в процентах')
    lamp_on_time = models.IntegerField('Время включения лампы в часах')
    lamp_off_time = models.IntegerField('Время выключения лампы в часах')
    pump_run_time = models.IntegerField('Время работы помпы в секундах')
    data_sending_frequency = models.IntegerField('Таймер отправки данных с платы в секундах')
    planting_date = models.CharField('Дата посадки в формате: 25.08.2020', max_length=20, null=True)
    days_before_harvest = models.IntegerField('Дней до предполагаемой технической спелости', null=True)


class GrowBoxDateTime(models.Model):
    year = models.IntegerField('Год')
    month = models.IntegerField('Месяц')
    day = models.IntegerField('День')
    hours = models.IntegerField('Часы')
    minutes = models.IntegerField('Минуты')
    seconds = models.IntegerField('Секунды')


class GrowBoxHistoricalData(models.Model):
    air_temperature = models.IntegerField('Температура воздуха')
    air_humidity = models.IntegerField('Влажность воздуха')
    soil_humidity = models.IntegerField('Влажность грунта')
    datetime = models.OneToOneField(GrowBoxDateTime, on_delete=models.CASCADE)
