from django.db import models

# Create your models here.

class Alert(models.Model):
    sensor_id = models.IntegerField()
    device_id = models.IntegerField()
    description = models.TextField()
    served = models.BooleanField()
    alert_id = models.IntegerField(primary_key=True)
    date = models.DateTimeField()
    priority = models.IntegerField()