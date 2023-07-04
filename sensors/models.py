from django.db import models

# Create your models here.

# Sensor types
SENSOR_CHOICES = [
    ('temperature', 'Temperature'),
    ('humidity', 'Humidity'),
]


class Sensor(models.Model):
    name = models.CharField(max_length=25)
    # dth_sensor = models.BooleanField() #This field is not going to the database. Checking it only means that two requests will be created in sensors/views.py
    type = models.CharField(choices=SENSOR_CHOICES, max_length=15)
    pin_number = models.IntegerField()
    min_value = models.IntegerField()
    max_value = models.IntegerField()
