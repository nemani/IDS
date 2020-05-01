from threading import Timer

import paho.mqtt.client as mqtt
import json
from datetime import datetime


class BaseDevice:
    def __init__(self, uuid, broker, dtype):
        self.dtype = dtype
        self.uuid = uuid

        self.client = mqtt.Client(f'{self.dtype} Device: ID {self.uuid}')
        self.client.connect(broker)

        self.topic = f"Devices/{self.uuid}"

        self.client.subscribe(self.topic)
        self.send_init_message()
        
    def send_init_message(self):
        message = self.create_message({'type': "New Device", 'content': f"New {self.dtype} device created!", 'dtype': self.dtype, 'group': self.group })
        self.client.publish("Devices", message)

    def create_message(self, message_opts):
        message = {}
        message['dtype'] = self.dtype
        message['uuid'] = self.uuid
        message['timestamp'] = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        message = {**message, **message_opts}
        return json.dumps(message)

    def on_message_recieve(self, client, userdata, message):
        data = json.loads(message.payload)

        if data.type == "Command":
            self.process_command(data)
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)

    def start(self):
        if not self.is_active:
            self._timer = Timer(self.tick_time, self.on_stimulus)
            self._timer.start()
            self.is_active = True

    def stop(self):
        self._timer.cancel()
        self.is_active = False

    def on_stimulus(self):
        self.is_active = False
        self.start()
        self.send_message()