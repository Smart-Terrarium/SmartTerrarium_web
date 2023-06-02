from django.forms import ModelForm, ChoiceField
from .models import Sensor, SENSOR_CHOICES


class SensorForm(ModelForm):
    type = ChoiceField(label='Sensor Type', choices=SENSOR_CHOICES)

    class Meta:
        model = Sensor
        fields = ['name', 'type', 'pin', 'min_value', 'max_value']
