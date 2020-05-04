from threading import Timer

import paho.mqtt.client as mqtt
import json
from datetime import datetime


class BaseDevice:
    def __init__(self, uuid, broker, dtype):
        self.dtype = dtype
        self.uuid = uuid

        self.client = mqtt.Client(f'{self.dtype} Device: ID {self.uuid}')
        self.client.on_message = self.on_message_recieve
        self.client.connect(broker)
        self.topic = f"Devices/{self.uuid}"

        self.client.subscribe(self.topic)
        print(f"BaseDevice: init {uuid} {dtype}")
        self.send_init_message()
        
    def send_init_message(self):
        message = self.create_message({'type': "New Device", 'content': f"New {self.dtype} device created!", 'dtype': self.dtype})
        print(message)
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
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic=", message.topic)

        if data.type == "Command":
            self.process_command(data)
        if data.type == "Control":
            if data.control == "Start Device":
                if self.is_active:
                    return
                self.start()
                self.start_heatbeat()
            elif data.control == "Stop Device":
                if not self.is_active:
                    return
                self.stop()
            elif data.control() == "Remove Device":
                if not self.is_active and not self.is_beating:
                    return
                self.stop()
                self.stop_heatbeat()

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

    def start_heatbeat(self):
        if not self.beating:
            self._timer = Timer(30, self.on_stimulus)
            self._timer.start()
            self.beating = True

    def stop_heatbeat(self):
        self._timer.cancel()
        self.beating = False

    def on_heatbeat(self):
        self.beating = False
        self.start()
        self.send_heartbeat()

    def send_heartbeat(self):
        message = self.create_message( {'type': 'Heartbeat'} )

        # Publish to Self Topic
        self.client.publish(self.topic, message)

        # Also Publish to all Devices Topic
        self.client.publish("Devices", message)
