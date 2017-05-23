# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from items import WechattopItem


class WechattopPipeline(object):
    def process_item(self, item, spider):
        return item
class PornhubMongoDBPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["WechatTop"]
        self.PhRes = db["PhRes"]

    def process_item(self, item, spider):
        print 'MongoDBItem', item
        """ 判断类型 存入MongoDB """
        if isinstance(item, WechattopItem):
            print 'WechattopItem True'
            try:
                self.PhRes.insert(dict(item))
            except Exception:
                pass
        return item
