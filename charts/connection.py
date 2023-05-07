import asyncio
import json
import websocket
import time

from django.shortcuts import render
from pychartjs import BaseChart, ChartType, Color

from charts import views

device_dict = {}
sensor_dict = {}
values_array = []
temp_array = []


class MyBarGraph(BaseChart):
    type = ChartType.Line

    class data:
        label = "Numbers"
        data = [12, 19, 3, 17, 10]
        backgroundColor = Color.Green

    class labels:
        grouped = [1, 2, 3, 4, 5]


class Sensor():
    def __init__(self, id, timestamp, value):
        self.id = id
        self.timestamp = timestamp
        self.value = value


class Device():
    def __init__(self, id):
        self.id = id
        self.sennsors = []

    def add(self, sensor):
        self.sennsors.append(sensor)


def parse(data):
    data = json.loads(data)
    data = json.loads(data)
    devices = []
    for device_id, sensors_data in data.items():
        device = Device(device_id)
        for sensor_id, sensor_data in sensors_data.items():
            sensor = Sensor(sensor_id, sensor_data['timestamp'], sensor_data['value'])
            device.add(sensor)
        devices.append(device)
    return devices


def json_to_array(devices):
    for device in devices:
        for sensor in device.sennsors:

            values_array = [sensor.timestamp, sensor.value]

            device_dict.setdefault(device.id, {}).update({})

            if len(device_dict[device.id]) < 8:
                device_dict[device.id][sensor.id] = [values_array]
            else:
                device_dict[device.id][sensor.id].append(values_array)

    print(device_dict)

    # views.get_data(device_dict)


async def ws_connection():
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:8000/data")
    while True:
        testdata = ws.recv()
        devices = parse(testdata)
        json_to_array(devices)


"""        for device in devices:
            print(device.id)
            for sennsor in device.sennsors:
                print(sennsor.timestamp)
                print(sennsor.id)
                print(sennsor.value)
                print("---")
            print("====")"""

if __name__ == "__main__":
    asyncio.run(ws_connection())
