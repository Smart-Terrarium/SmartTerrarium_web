from django.forms import ModelForm, ChoiceField
from .models import Sensor, SENSOR_CHOICES


class SensorForm(ModelForm):
    type = ChoiceField(label='Sensor Type', choices=SENSOR_CHOICES)  # Field for selecting sensor type

    class Meta:
        model = Sensor
        fields = ['name', 'type', 'pin_number', 'min_value', 'max_value']  # Fields to include in the form
