# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class ScrapyDemoPipeline(object):
    def process_item(self, item, spider):
        print('------拿到了item',item['name'])
        return item

class MongoPipeline(object):

    # collection = 'lianjia'
    collection = 'avengers'


    def __init__(self,mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.count = 0

    @classmethod
    def from_crawler(cls, crawler):
        """
        初始化时候，用于创建pipeline对象
        :param crawler:
        :return:
        """
        mongo_url = crawler.settings.get('MONGO_URI')
        mongo_db = crawler.settings.get('MONGO_DB')

        return cls(mongo_url, mongo_db)

    def open_spider(self,spider):
        """
        爬虫开始执行时，调用
        :param spider:
        :return:
        """
        self.client = MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        """
        爬虫关闭时，被调用
        :param spider:
        :return:
        """
        print(self.count)
        self.client.close()

    def process_item(self, item, spider):
        """
        每当数据需要持久化时，就会被调用
        :param item:
        :param spider:
        :return:
        """
        table = self.db[self.collection]
        data = dict(item)
        self.count += 1
        print('count',self.count)
        table.insert_one(data)
        return item