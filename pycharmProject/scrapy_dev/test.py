
from pymongo import MongoClient

client=MongoClient('mongodb://localhost:27017')

db=client['runoob']

table = db['lpl']

table.insert_one({"name":"clearlove","id":1,"team":"edg"})

client.close()