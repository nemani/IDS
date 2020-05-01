import dataset

db = dataset.connect('postgresql://postgres@localhost:5432/device_manager')

device_table = db['device']
data_table = db['data']

