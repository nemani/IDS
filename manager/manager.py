import json
from datetime import datetime

import paho.mqtt.client as mqtt
from kafka import KafkaProducer, KafkaConsumer

from database import db

class DeviceManager():
    def __init__(self, broker):
        self.broker = broker
        self.kafka_producer = KafkaProducer(bootstrap_servers=f"{broker}:9092", value_serializer=lambda x: json.dumps(x).encode('utf-8'))

        self.client = mqtt.Client(f'Device Manager')
        self.client.on_message = self.on_mqtt_message_recieve
        self.topic = "DeviceManager"

        self.client.connect(broker)
        self.client.subscribe(self.topic)
        self.client.subscribe("Devices")
    
    def on_mqtt_message_recieve(self, client, userdata, message):
        data = json.loads(message.payload)
        print(data)

    def add_device(self, data):
        if db['device'].find_one(uuid=data['uuid']):
            return False

        device = {}
        device['uuid'] = data['uuid']
        device['dtype'] = data['dtype']
        device['group'] = data['group']
        device['created_at'] = datetime.now()
        db['device'].insert(device)
        self.init_new_device(data['uuid'], data['dtype'])
        return True
    
    def init_new_device(self, uuid, dtype):
        message = {}
        message['uuid'] = uuid
        message['dtype'] = dtype

        message['type'] = 'Command'
        message['Command'] = 'Add Device'

        message = json.dumps(message)
        self.client.publish('Devices', message)

    def remove_device(self, device_id):
        db['device'].delete(uuid=device_id)

    def list_devices(self):
        devices = {}
        for device in db['device'].find():
            device["created_at"] = device["created_at"].strftime("%d/%m/%y %H:%M:%S")
            devices[device['id']] = device

        return devices
    
    def get_device(self, device_id):
        device = db['device'].find_one(uuid=device_id)
        
        if not device:
            return None

        device["created_at"] = device["created_at"].strftime("%d/%m/%y %H:%M:%S")
        return device
    
    def list_groups(self):
        groups = {}
        
        for device in db['device'].find():
            device["created_at"] = device["created_at"].strftime("%d/%m/%y %H:%M:%S")
            group = device['group']
            
            if group in groups:
                groups[group].append(device)
            else:
                groups[group] = [device]

        return groups
    
