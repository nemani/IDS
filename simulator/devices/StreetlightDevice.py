import random
from .BaseDevice import BaseDevice

class StreetlightDevice(BaseDevice):
    def __init__(self, uuid, broker):
        self.tick_time = 1
        self.is_active = False
        BaseDevice.__init__(self, uuid, broker, 'Streetlight')

    def process_command(self, data):
        print(data)

    def send_message(self):
        streetlight_simulation = random.choices([0, 1], [5, 95])
        message = self.create_message( {'type': 'Tick', 'value': streetlight_simulation[0]} )
        
        # Publish to Self Topic
        self.client.publish(self.topic, message)

        # Also Publish to all Devices Topic
        self.client.publish("Devices", message)