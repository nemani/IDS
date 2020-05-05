import random
from .BaseDevice import BaseDevice

class AttendanceDevice(BaseDevice):
    def __init__(self, uuid, broker):
        self.tick_time = 30
        self.is_active = False
        BaseDevice.__init__(self, uuid, broker, 'Attendance')

    def process_command(self, data):
        print(data)

    def send_message(self):
        attendance_simulation = random.choices([((30, 70), (150, 250)), ((
            50, 100), (100, 150)), ((30, 50), (80, 100))], [60, 20, 20])
        message = self.create_message({
            'type': 'Tick', 
            'value': random.randrange(attendance_simulation[0][0][0], attendance_simulation[0][0][1]),
            'value2': random.randrange(attendance_simulation[0][1][0], attendance_simulation[0][1][1])
        })

        # Publish to Self Topic
        self.client.publish(self.topic, message)

        # Also Publish to all Devices Topic
        self.client.publish("Devices", message)