from django.shortcuts import render, redirect
from .forms import SensorForm
import requests
import json


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
