from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from requests import RequestException

from .forms import SensorForm
import requests
import json

from .models import Sensor, SENSOR_CHOICES

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
            try:
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
                            context = {'form': form, 'error_message': 'Failed to create sensor.'}
                            return render(request, 'new_sensor.html', context)
                    else:
                        context = {'form': form, 'error_message': 'No devices found for the user.'}
                        return render(request, 'new_sensor.html', context)
                else:
                    context = {'form': form, 'error_message': 'Failed to retrieve device ID.'}
                    return render(request, 'new_sensor.html', context)
            except requests.RequestException:
                context = {'form': form, 'error_message': 'Connection lost. Please try again later.'}
                return render(request, 'new_sensor.html', context)

    else:
        form = SensorForm()

    return render(request, 'new_sensor.html', {'form': form})


@login_required
def select_sensors(request):
    access_token = request.session.get('access_token')
    context = {
        'access_token': access_token,
        'text': 'Error - connection to server failed',
        'sensor_types': SENSOR_CHOICES,
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

                        # Prepare sensors using the Sensor model but don't save to the database
                        sensor_data = []
                        for sensor_data_json in sensor_response_json:
                            sensor = Sensor(
                                id=sensor_data_json['id'],
                                name=sensor_data_json['name'],
                                type=sensor_data_json['type'],
                                pin_number=sensor_data_json['pin_number'],
                                min_value=sensor_data_json['min_value'],
                                max_value=sensor_data_json['max_value'],
                                device_id=device_id,  # Add device_id to the sensor data
                            )
                            sensor_data.append(sensor)

                        context['sensor_data'] = sensor_data
                        context['device_id'] = device_id  # Add device_id to the context

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

@login_required
def delete_sensor(request, sensor_id, device_id):
    if request.method == 'POST':
        access_token = request.session.get('access_token')
        bearer_token = 'Bearer ' + access_token

        delete_url = API_URL + f'device/{device_id}/sensor/{sensor_id}'
        headers = {'Authorization': bearer_token}

        try:
            response = requests.delete(delete_url, headers=headers)
            if response.ok:
                return redirect('sensors')
            else:
                error_message = 'Failed to delete sensor.'
                context = {'error_message': error_message}
                return render(request, 'sensors.html', context)

        except requests.RequestException:
            error_message = 'Connection lost. Please try again.'
            context = {'error_message': error_message}
            return render(request, 'sensors.html', context)

    else:
        return render(request, 'sensors.html')


@login_required
def edit_sensor(request, device_id, sensor_id):
    if request.method == 'POST':
        access_token = request.session.get('access_token')
        bearer_token = 'Bearer ' + access_token

        # Pobranie danych z formularza
        name = request.POST.get('name')
        pin_number = int(request.POST.get('pin_number'))
        type = request.POST.get('type')
        min_value = float(request.POST.get('min_value'))
        max_value = float(request.POST.get('max_value'))

        # Utworzenie JSON z nowymi danymi dla sensora
        sensor_data = {
            'name': name,
            'pin_number': pin_number,
            'type': type,
            'min_value': min_value,
            'max_value': max_value,
        }

        # Utworzenie nagłówka z tokenem dostępu
        headers = {'Authorization': bearer_token}

        # Wysłanie żądania PUT na adres edycji sensora
        edit_url = f'http://localhost:8000/device/{device_id}/sensor/{sensor_id}/'
        try:
            response = requests.put(edit_url, json=sensor_data, headers=headers)
            if response.ok:
                return redirect('sensors')
            else:
                error_message = 'Failed to edit sensor.'
                context = {'error_message': error_message}
                return render(request, 'sensors.html', context)

        except requests.RequestException:
            error_message = 'Connection lost. Please try again.'
            context = {'error_message': error_message}
            return render(request, 'sensors.html', context)

    else:
        # Pobranie danych o sensorze z API
        access_token = request.session.get('access_token')
        headers = {'Authorization': 'Bearer ' + access_token}

        get_url = f'http://localhost:8000/device/{device_id}/sensor/{sensor_id}/'
        try:
            response = requests.get(get_url, headers=headers)
            if response.ok:
                sensor_data = response.json()
                # Dodaj pole 'sensor_types' do kontekstu
                context = {'sensor_data': sensor_data, 'sensor_types': SENSOR_CHOICES}
                return render(request, 'sensors.html', context)
            else:
                error_message = 'Failed to retrieve sensor data.'
                context = {'error_message': error_message}
                return render(request, 'sensors.html', context)

        except requests.RequestException:
            error_message = 'Connection lost. Please try again.'
            context = {'error_message': error_message}
            return render(request, 'sensors.html', context)

