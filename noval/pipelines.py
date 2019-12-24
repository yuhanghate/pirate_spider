# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys

from noval.DBHelper import DBHelper
from noval.items import BooksItem, ChapterItem, ContentItem, BooksDeleteItem


class NovalPipeline(object):

    # 开启爬虫时执行，只执行一次
    def open_spider(self, spider):
        self.db = DBHelper()
        pass

    def process_item(self, item, spider):
        # print(dict(item))
        data = json.dumps(dict(item), ensure_ascii=False)
        print(data)

        # 插入数据库
        if isinstance(item, BooksItem):
            self.db.insertBooks(item)
        if isinstance(item, ChapterItem):
            self.db.insertChapters(item)
        if isinstance(item, ContentItem):
            self.db.insertContent(item)
        if isinstance(item, BooksDeleteItem):
            self.db.updateDeleteFlagByBooks(item)
        pass

    def close_spider(self, spider):
        self.db.cursor.close()
        pass
