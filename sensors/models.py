from django.db import models

# Sensor types
SENSOR_CHOICES = [
    ('temperature', 'Temperature'),
    ('humidity', 'Humidity'),
]

class Sensor(models.Model):
    device_id = models.IntegerField()            # ID of the associated device
    id = models.IntegerField(primary_key=True)   # Primary key for the sensor
    name = models.CharField(max_length=25)       # Name of the sensor
    dth_sensor = models.BooleanField()           # Not stored in the database, used for creating requests
    type = models.CharField(max_length=15, choices=SENSOR_CHOICES)  # Type of the sensor
    pin_number = models.IntegerField()           # Pin number for the sensor
    min_value = models.IntegerField()            # Minimum value for the sensor
    max_value = models.IntegerField()            # Maximum value for the sensor
