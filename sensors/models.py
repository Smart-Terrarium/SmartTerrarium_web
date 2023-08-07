from django.db import models

# Sensor types
SENSOR_CHOICES = [
    ('temperature', 'Temperature'),
    ('humidity', 'Humidity'),
]

class Sensor(models.Model):
    device_id = models.IntegerField()
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25)
    # dth_sensor = models.BooleanField() #This field is not going to the database. Checking it only means that two requests will be created in sensors/views.py
    type = models.CharField(max_length=15, choices=SENSOR_CHOICES)
    pin_number = models.IntegerField()
    min_value = models.IntegerField()
    max_value = models.IntegerField()
