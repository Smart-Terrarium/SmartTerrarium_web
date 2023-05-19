import asyncio
import json
import websocket
import time
import pychartjs
from pychartjs import Options
import importlib
import time
from charts import views

import websocket
from django.shortcuts import render
from pychartjs import BaseChart, ChartType, Color

device_dict = {}




def parse(data):
    # Konwersja danych JSON na słownik Pythona
    data = json.loads(data)

    for device_id in data: # iteracja po kluczach w słowniku data
        # Utworzenie nowego słownika dla urządzenia, jeśli nie istnieje
        device_dict.setdefault(device_id, {}).update({})
        for sensor_id in data[device_id]: # iteracja po kluczach w słowniku dla danego urządzenia
            # Dodanie nowego czujnika dla urządzenia, jeśli nie istnieje
            device_dict[device_id].setdefault(sensor_id, []).append(
                [data[device_id][sensor_id]['timestamp'], data[device_id][sensor_id]['value']])
            # Jeśli liczba wartości przekracza 5, usunięcie najstarszej wartości z listy
            if len(device_dict[device_id][sensor_id]) > 5:
                device_dict[device_id][sensor_id].pop(0)
    return device_dict
    # Zwrócenie słownika device_dict
    '''Poniżej wylistowanie tylko danych z pierwszego urządzenia z pierwszego sensora
    return device_dict[list(device_dict.keys())[0]][list(device_dict[list(device_dict.keys())[0]].keys())[0]]'''

    """
    Poniżej wylistowanie tylko timestamp z pierwszego urządzenia z pierwszego sensora
    first_device = list(device_dict.keys())[0]
    first_sensor = list(device_dict[first_device].keys())[0]
    return [value[0] for value in device_dict[first_device][first_sensor]]"""



#Wykres pyChart.js
class MyBarGraph(BaseChart):
    type = ChartType.Line

    class labels:
        xAxis = [1,2]



    class data:
        class Whales:
            data = [80, 60, 100, 80, 90, 60]
            backgroundColor = Color.Gray

        class Bears:
            data = [60, 50, 80, 120, 140, 180]
            backgroundColor = Color.Blue

        class Dolphins:
            data = [150, 80, 60, 30, 50, 30]
            backgroundColor = Color.Orange

    class options:
        title = {"text": "Wildlife Populations",
                 "display": True}


#Połącznie z websocket
async def ws_connection():
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:8000/data")
    while True: #dodać czekanie co sekundę
        testdata = ws.recv()
        #Wyprintowanie funkcji 'parse', która jako argument dostaje 'testdata = ws.recv()'
        print(parse(testdata))



if __name__ == "__main__":
    asyncio.run(ws_connection())