from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from requests import RequestException

from .forms import SensorForm
import requests
import json

from .models import Sensor

API_URL = 'http://localhost:8000/'


@login_required
def create_sensor(request):
    if request.method == 'POST':
        form = SensorForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            bearer_token = request.session.get('access_token')
            headers = {
                'Authorization': 'Bearer ' + bearer_token,
            }

            # GET request to receive device id of a user
            device_id_response = requests.get('http://localhost:8000/devices/', headers=headers)
            if device_id_response.ok:
                devices_data = device_id_response.json()
                if len(devices_data) > 0:
                    device_id = devices_data[0]['id']

                    url = f'http://localhost:8000/device/{device_id}/sensor/'
                    response = requests.post(url, data=json.dumps(data), headers=headers)

                    if response.ok:
                        return redirect('home')  # Przekierowanie po udanym żądaniu
                    else:
                        return redirect('blad')  # Przekierowanie po błędnym żądaniu
                else:
                    return redirect('blad')  # Przekierowanie w przypadku braku urządzenia
            else:
                return redirect('blad')  # Przekierowanie w przypadku nieudanego żądania GET na /devices

    else:
        form = SensorForm()

    return render(request, 'new_sensor.html', {'form': form})


@login_required
def select_sensors(request):
    access_token = request.session.get('access_token')
    context = {
        'access_token': access_token,
        'text': 'Error - connection to server failed'
    }

    headers = {
        'Authorization': 'Bearer ' + access_token,
    }
    try:
        devices_response = requests.get('http://localhost:8000/devices/', headers=headers)
        if devices_response.ok:
            response_json = devices_response.json()
            if isinstance(response_json, list) and len(response_json) > 0:
                device_id = response_json[0].get('id')
                if device_id:
                    sensor_response = requests.get(f'http://localhost:8000/device/{device_id}/sensor', headers=headers)
                    if sensor_response.ok:
                        sensor_response_json = sensor_response.json()
                        # Pass the sensor data directly to the template
                        context['sensor_data'] = sensor_response_json
                    else:
                        context['error_message'] = 'Error retrieving sensor data for the device.'
                else:
                    context['error_message'] = 'Invalid device ID.'
            else:
                context['error_message'] = 'Invalid response format - missing or empty list of devices.'
        else:
            context['error_message'] = 'Connection lost. Please log in again to see your devices.'
    except requests.RequestException:
        context['error_message'] = 'Connection lost. Please log in again to see your devices.'

    return render(request, 'sensors.html', context)