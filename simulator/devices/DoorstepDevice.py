import random
from .BaseDevice import BaseDevice

class DoorstepDevice(BaseDevice):
    def __init__(self, uuid, broker):
        self.tick_time = 1
        self.is_active = False
        BaseDevice.__init__(self, uuid, broker, 'Doorstep')

    def process_command(self, data):
        print(data)

    def send_message(self):
        doorstep_simulation = random.choices([0, 1], [90, 10])
        message = self.create_message( {'type': 'Tick', 'value': doorstep_simulation[0]} )
        
        # Publish to Self Topic
        self.client.publish(self.topic, message)

        # Also Publish to all Devices Topic
        self.client.publish("Devices", message)