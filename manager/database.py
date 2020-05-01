import dataset

db = dataset.connect('postgres://dsrtthoz:v9o8xiTeDjaE38CjDjXtUXkav-xD4tO0@drona.db.elephantsql.com:5432/dsrtthoz')

device_table = db['device']
data_table = db['data']

