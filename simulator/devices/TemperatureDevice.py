import random
from .BaseDevice import BaseDevice

class TemperatureDevice(BaseDevice):
    def __init__(self, uuid, broker):
        self.tick_time = 30
        self.is_active = False
        BaseDevice.__init__(self, uuid, broker, 'Temperature')

    def process_command(self, data):
        print(data)

    def send_message(self):
        temperature_simulation = random.choices([(10, 59), (60, 100), (101, 120), (200, 220)], [20, 60, 15, 5])
        message = self.create_message({'type': 'Tick', 'Temperature': random.randrange(temperature_simulation[0][0], temperature_simulation[0][1])})
        
        # Publish to Self Topic
        self.client.publish(self.topic, message)

        # Also Publish to all Devices Topic
        self.client.publish("Devices", message)
