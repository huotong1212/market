from datetime import datetime

from pymongo import MongoClient
#
# client=MongoClient('mongodb://localhost:27017')
#
# db=client['runoob']
#
# table = db['lpl']
#
# table.insert_one({"name":"clearlove","id":1,"team":"edg"})
#
# client.close()

# import time
# import datetime
#
# now = datetime.datetime.now()
# print(now)
# print(type(now.strftime('%Y-%m-%d')))

client = MongoClient('mongodb://localhost:27017')
db = client['test']
collection = db['onetomany']

from scrapy_demo.items import CommentItem,SanshengItem

sitem = SanshengItem()
sitem['price'] = 70
sitem['name'] = '三生三世'
sitem['comments'] = '赵丽颖'

citme = CommentItem()
citme['title'] = '电视剧'
citme['rating'] = 5
citme['time'] = datetime.now().strftime('%Y-%m-%d')

sitem['comments'] = dict(citme)
sitem['comments'] = citme

print(dict(sitem))
sstime = dict(sitem)
print(type(sstime['comments']))
print(dict(citme))

collection.insert_one(sstime)
client.close()
#
# x = ' 132 1  '
# print(x.strip())