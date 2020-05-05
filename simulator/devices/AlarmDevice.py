import random
from .BaseDevice import BaseDevice

class AlarmDevice(BaseDevice):
    def __init__(self, uuid, broker):
        self.tick_time = 1
        self.is_active = False
        self.alarm = 0
        BaseDevice.__init__(self, uuid, broker, 'Alarm')

    def process_command(self, data):
        print(data)

    def send_message(self):
        message = self.create_message({'type': 'Tick', 'value': self.alarm})
        # Publish to Self Topic
        self.client.publish(self.topic, message)

        # Also Publish to all Devices Topic
        self.client.publish("Devices", message)
