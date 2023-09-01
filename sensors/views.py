from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, reverse, render
from requests import RequestException
from django.contrib import messages
from .forms import SensorForm
import requests
import json
from django.conf import settings

from .models import Sensor, SENSOR_CHOICES

API_URL = settings.API_URL


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

            # Send a GET request to fetch the device ID associated with the user's account
            try:
                device_id_response = requests.get(settings.API_URL + 'devices', headers=headers)
                if device_id_response.ok:
                    devices_data = device_id_response.json()
                    if len(devices_data) > 0:
                        # Get the device ID from the first device in the list
                        device_id = devices_data[0]['id']
                        # Construct the URL for creating a new sensor under the device
                        url = f'{settings.API_URL}device/{device_id}/sensor/'
                        response = requests.post(url, data=json.dumps(data), headers=headers)

                        if response.ok:
                            messages.success(request,'Sensor created successfully! '
                                                     'Remember to synchronize changes with your device.')
                            return redirect('sensors')  # Redirect after successful request
                        else:
                            context = {'form': form, 'error_message': 'Failed to create sensor. Probably sensor with given informations already exists'}
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
def create_dht_sensor(request):
    if request.method == 'POST':
        # Extract form data for temperature sensor form
        temperature_name = request.POST.get('temperature_name')
        temperature_min_value = request.POST.get('temperature_min_value')
        temperature_max_value = request.POST.get('temperature_max_value')
        temperature_sensor_type = 'temperature'

        # Extract form data for humidity sensor form
        humidity_name = request.POST.get('humidity_name')
        humidity_min_value = request.POST.get('humidity_min_value')
        humidity_max_value = request.POST.get('humidity_max_value')
        humidity_sensor_type = 'humidity'

        # Extract pin number from form
        pin_number = request.POST.get('pin_number')

        try:
            # Get the access token from the user's session
            bearer_token = request.session.get('access_token')
            headers = {
                'Authorization': 'Bearer ' + bearer_token,
            }

            # Send a GET request to receive the device ID of a user
            device_id_response = requests.get(settings.API_URL + 'devices', headers=headers)
            if device_id_response.ok:
                devices_data = device_id_response.json()
                if len(devices_data) > 0:
                    device_id = devices_data[0]['id']

                    # Prepare data for API requests
                    temperature_data = {
                        'name': temperature_name,
                        'type': temperature_sensor_type,
                        'min_value': temperature_min_value,
                        'max_value': temperature_max_value,
                        'pin_number': int(pin_number) * 100 + 1
                    }

                    humidity_data = {
                        'name': humidity_name,
                        'type': humidity_sensor_type,
                        'min_value': humidity_min_value,
                        'max_value': humidity_max_value,
                        'pin_number': int(pin_number) * 100 + 2
                    }

                    # Make API requests to create temperature and humidity sensors
                    temperature_response = requests.post(
                        f'{settings.API_URL}device/{device_id}/sensor/',
                        json=temperature_data,
                        headers=headers,
                        verify=False
                    )

                    humidity_response = requests.post(
                        f'{settings.API_URL}device/{device_id}/sensor/',
                        json=humidity_data,
                        headers=headers
                    )

                    # Handle responses and render appropriate template
                    if temperature_response.status_code == 201 and humidity_response.status_code == 201:
                        messages.success(request, 'DHT sensor created successfully! Remember to synchronize changes with your device.')
                        return redirect('sensors')
                    else:
                        context = {'error_message': 'Failed to create sensors. '
                                                    'Probably sensors with given informations already exists'}
                        return render(request, 'new_dht_sensor.html', context)

        except requests.RequestException:
            context = {'error_message': 'Connection lost. Please try again later.'}
            return render(request, 'new_dht_sensor.html', context)

    return render(request, 'new_dht_sensor.html')
@login_required
def select_sensors(request):
    # Get the access token from the user's session
    access_token = request.session.get('access_token')
    # Prepare the initial context with access token and sensor types
    context = {
        'access_token': access_token,
        'text': 'Error - connection to server failed',
        'sensor_types': SENSOR_CHOICES,
    }
    headers = {
        'Authorization': 'Bearer ' + access_token,
    }
    try:
        # Send a GET request to fetch the list of devices associated with the user
        devices_response = requests.get(settings.API_URL + 'devices', headers=headers)
        if devices_response.ok:
            response_json = devices_response.json()
            if isinstance(response_json, list) and len(response_json) > 0:
                device_id = response_json[0].get('id')
                if device_id:
                    # Send a GET request to fetch sensor data for the selected device
                    sensor_response = requests.get(f'{settings.API_URL}device/{device_id}/sensor', headers=headers)
                    if sensor_response.ok:
                        sensor_response_json = sensor_response.json()

                        # Prepare sensor data using the Sensor model but don't save to the database
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
                        # Update the context with sensor data and device ID
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
        # Prepare the headers for the DELETE request
        headers = {'Authorization': bearer_token}

        try:
            # Send a DELETE request to remove the sensor
            response = requests.delete(delete_url, headers=headers)
            if response.ok:
                messages.success(request,
                                 'The sensor has been removed. Remember to synchronize changes with your device.')
                return redirect('sensors')
            else:
                messages.error(request,
                                 'The sensor cannot be removed. There is an alert for this sensor in the database. '
                                 'First remove the alert and try removing the sensor again.')
                return redirect('sensors')

        except requests.RequestException:
            messages.error(request,
                           'Connection lost. Please try again.')
            return redirect('sensors')

    else:
        return render(request, 'sensors.html')


@login_required
def edit_sensor(request, device_id, sensor_id):
    if request.method == 'POST':
        access_token = request.session.get('access_token')
        bearer_token = 'Bearer ' + access_token

        # Get data from the form
        name = request.POST.get('name')
        pin_number = int(request.POST.get('pin_number'))
        type = request.POST.get('type')
        min_value = float(request.POST.get('min_value'))
        max_value = float(request.POST.get('max_value'))

        # Create JSON data with the new sensor information
        sensor_data = {
            'name': name,
            'pin_number': pin_number,
            'type': type,
            'min_value': min_value,
            'max_value': max_value,
        }

        # Prepare headers with the access token
        headers = {'Authorization': bearer_token}

        # Construct the URL for the PUT request to edit the sensor
        edit_url = f'{settings.API_URL}device/{device_id}/sensor/{sensor_id}/'
        try:
            # Send a PUT request to edit the sensor
            response = requests.put(edit_url, json=sensor_data, headers=headers)
            if response.ok:
                messages.success(request,
                                 'You have edited the sensor successfully! Remember to synchronize changes with your device.')
                return redirect('sensors')
            else:
                messages.error(request,
                               'Failed while trying to edit sensor. Please try again.')
                return redirect('sensors')

        except requests.RequestException:
            messages.error(request,
                           'Connection lost. Please try again.')
            return redirect('sensors')


@login_required
def sync_sensors_with_db(request, device_id):
    access_token = request.session.get('access_token')
    bearer_token = 'Bearer ' + access_token

    sync_url = f'{settings.API_URL}device/{device_id}/sensors/'
    headers = {'Authorization': bearer_token}

    try:
        response = requests.post(sync_url, headers=headers)
        if response.ok:
            messages.success(request, 'Sensors synchronized successfully!')
        else:
            messages.error(request, 'Failed to synchronize sensors with the database.')

    except requests.RequestException:
        messages.error(request, 'Connection lost. Please try again.')

    return redirect('sensors')