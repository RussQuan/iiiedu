# -*- coding: utf-8 -*-

from scrapy.contrib.exporter import JsonItemExporter
from time import sleep
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



class iiieduJsonPipeline(object):
    def __init__(self):
        self.file = open("data1.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item



class iiieduMongoPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'])
        db = connection[settings['MONGODB_DB']]
        self.collection_iiiedu = db[settings['MONGODB_COLLECTION_IIIEDU']]
        self.collection_uplist_iiiedu = db[settings['MONGODB_COLLECTION_UPLIST']]


    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            link = item['link']
            Class_ID = item['Class_ID']

            result = self.collection_iiiedu.find_one({'link': link}, {"Class_ID": 1, "_id": 0})
            print(result)

            if not result:
                self.collection_iiiedu.insert(dict(item))
                sleep(1)
                self.collection_uplist_iiiedu.insert(dict(item))
                print("新增%s" % Class_ID)
            else:
                print("已存在%s" % Class_ID)

            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
