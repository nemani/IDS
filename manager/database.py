import dataset

# db = dataset.connect('postgresql://postgres@localhost:5432/device_manager')
db = dataset.connect('postgres://dsrtthoz:v9o8xiTeDjaE38CjDjXtUXkav-xD4tO0@drona.db.elephantsql.com:5432/dsrtthoz')

device_table = db['device']
data_table = db['data']

