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
        self.client.loop_start()
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
        message['created_at'] = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        message = {**message, **message_opts}
        return json.dumps(message)

    def on_message_recieve(self, client, userdata, message):
        if message.topic != self.topic:
            return
        data = json.loads(message.payload.decode("utf-8"))
        if data['type'] == "Control" and data['control'] == "Stop Device":
            self.stop()
            self.stop_heartbeat()
        if data['type'] == "Command":
            self.process_command(data)
                            
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

    def start_heartbeat(self):
        if not self.beating:
            self._heart_timer = Timer(30, self.on_heartbeat)
            self._heart_timer.start()
            self.beating = True

    def stop_heartbeat(self):
        self._heart_timer.cancel()
        self.beating = False

    def on_heartbeat(self):
        self.beating = False
        self.start_heartbeat()
        self.send_heartbeat()

    def send_heartbeat(self):
        message = self.create_message( {'type': 'Heartbeat'} )

        # Also Publish to all Devices Topic
        self.client.publish("Devices", message)
 