import argparse
import threading
import json 

import paho.mqtt.client as mqtt

from devices.TemperatureDevice import TemperatureDevice
from devices.AlarmDevice import AlarmDevice
from devices.DoorstepDevice import DoorstepDevice
from devices.AttendanceDevice import AttendanceDevice
from devices.TrafficDevice import TrafficDevice
from devices.StreetlightDevice import StreetlightDevice
from devices.ParkingDevice import ParkingDevice

parser = argparse.ArgumentParser(description='Start a new Device Simulator')
parser.add_argument('--broker', type=str, help='Broker Host to connect to', required=True)
args = parser.parse_args()
broker = args.broker

DEVICE_TYPES = {
    'Temperature': TemperatureDevice,
    'Doorstep': DoorstepDevice,
    'Attendance': AttendanceDevice,
    'Alarm': AlarmDevice,
    'Traffic': TrafficDevice,
    'Streetlight': StreetlightDevice,
    'Parking': ParkingDevice
}

def boot(uuid, dtype):
    device = DEVICE_TYPES[dtype](uuid, broker)
    device.on_stimulus()

def setup_device(uuid, dtype):
    thread = threading.Thread(target=boot, args=(uuid, dtype))
    thread.start()
    
def main_on_message_recieve(client, userdata, message):
    data = json.loads(message.payload)
    print(data)
    if data['type'] == 'Command':
        if data['command'] == 'Add Device':
            setup_device(data['uuid'], data['dtype'])


if __name__ == '__main__':
    main_client = mqtt.Client(f'Device Simulator')
    main_client.on_message = main_on_message_recieve
    main_client.connect(args.broker)
    main_client.subscribe('Devices')
    print('Simulator Started')
    print('Watching on Topic: Devices')

    main_client.loop_forever()
