import random
from .BaseDevice import BaseDevice

class ParkingDevice(BaseDevice):
    def __init__(self, uuid, broker):
        self.tick_time = 300
        self.is_active = False
        BaseDevice.__init__(self, uuid, broker, 'Parking')

    def process_command(self, data):
        print(data)

    def send_message(self):
        parking_simulation = random.choices([(0, 15), (16, 60), (61, 90), (91, 100)], [10, 60, 20, 10])
        message = self.create_message({
            'type': 'Tick',
            'value': random.randrange(parking_simulation[0][0], parking_simulation[0][1])
        })
        
        # Publish to Self Topic
        self.client.publish(self.topic, message)

        # Also Publish to all Devices Topic
        self.client.publish("Devices", message)