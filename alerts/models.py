from django.db import models

# Create your models here.

class Alert(models.Model):
    sensor_id = models.IntegerField()  # Identifier of the sensor triggering the alert
    device_id = models.IntegerField()  # Identifier of the device associated with the alert
    description = models.TextField()   # Description or details of the alert
    served = models.BooleanField()     # Indicates if the alert has been addressed/served
    alert_id = models.IntegerField(primary_key=True)  # Unique identifier for the alert
    date = models.DateTimeField()      # Date and time when the alert was generated
    priority = models.IntegerField()   # Priority level of the alert
