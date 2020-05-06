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
        self.init_db_devices()

    def init_db_devices(self):
        devices = self.list_devices()
        for idx, device in devices.items():
            if device['status'] == '1':
                self.send_add_message(device['uuid'], device['dtype'])

    def on_mqtt_message_recieve(self, client, userdata, message):
        data = json.loads(message.payload)
        data['uuid'] = int(data['uuid'])
        print(data['type'])
        if data['type'] == 'Heartbeat':
            data = dict(uuid=data['uuid'], heartbeat=datetime.now())
            db['device'].update(data, ['uuid'])
        elif data['type'] == 'Tick':
            data['created_at'] = datetime.strptime(data['created_at'], '%d/%m/%y %H:%M:%S')
            db['data'].insert(data, ensure=True)
            self.kafka_producer.send('DeviceManager', json.dumps(data))

    def add_device_to_db(self, data):
        if db['device'].find_one(uuid=data['uuid']):
            return False

        device = {}
        device['uuid'] = int(data['uuid'])
        device['dtype'] = data['dtype']
        device['group'] = int(data['group'])
        device['created_at'] = datetime.now()
        device['heartbeat'] = datetime.now()
        device['status'] = '1'
        db['device'].insert(device)
        return True

    def remove_device_from_db(self, uuid):
        if not db['device'].find_one(uuid=uuid):
            return False
        db['device'].delete(uuid=uuid)

    def send_add_message(self, uuid, dtype):
        message = {}
        message['uuid'] = uuid
        message['dtype'] = dtype
        message['type'] = 'Command'
        message['command'] = 'Add Device'
        message = json.dumps(message)
        self.client.subscribe(f'Devices/{uuid}')
        self.client.publish('Devices', message)

    def send_stop_message(self, uuid):
        message = {}
        message['uuid'] = uuid
        message['type'] = 'Control'
        message['control'] = 'Stop Device'
        message = json.dumps(message)
        self.client.publish(f'Devices/{uuid}', message)

    def update_status_off(self, uuid):
        device = self.get_device(uuid)
        data = dict(uuid=uuid, status='0')
        db['device'].update(data, ['uuid'])

    def update_status_on(self, uuid):
        device = self.get_device(uuid)
        data = dict(uuid=uuid, status='1')
        db['device'].update(data, ['uuid'])

    def list_devices(self):
        devices = {}
        for device in db['device'].find():
            device["created_at"] = device["created_at"].strftime("%d/%m/%y %H:%M:%S")
            devices[device['uuid']] = device
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

    def list_dtypes(self):
        dtypes = {}
        for device in db['device'].find():
            device["created_at"] = device["created_at"].strftime("%d/%m/%y %H:%M:%S")
            dtype = device['dtype']

            if dtype in dtypes:
                dtypes[dtype].append(device)
            else:
                dtypes[dtype] = [device]
        return dtypes

    def process_device_command(self, device, command):
        if command == "start":
            self.send_add_message(device['uuid'], device['dtype'])
            self.update_status_on(device['uuid'])
        if command == "stop":
            self.send_stop_message(device['uuid'])
            self.update_status_off(device['uuid'])
        if command == "delete":
            self.send_stop_message(device['uuid'])
            self.remove_device_from_db(device['uuid'])

    def get_device_data(self, device_uuid):
        val1 = {}
        val1['name'] = 'value1'
        val1['data'] = []
        val2 = {}
        val2['name'] = 'value2'
        val2['data'] = []
        q = f'SELECT created_at, value, value2 from data where uuid={device_uuid}'
        for each in db.query(q):
            time = each["created_at"].strftime("%d/%m/%y %H:%M:%S")
            point = [time, each['value'] ]
            val1['data'].append(point)
            if each['value2']:
                point = [time, each['value2'] ]
                val2['data'].append(point)
        
        if val2['data']:
            return [val1, val2]

        return val1['data']
