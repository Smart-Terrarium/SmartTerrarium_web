import json
from channels.generic.websocket import WebsocketConsumer
from random import randint
from time import sleep


class ChartsConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()

        for i in range(1000):
            self.send(json.dumps({'value': randint(-20, 20)}))
            sleep(1)