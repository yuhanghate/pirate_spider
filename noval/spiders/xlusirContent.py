# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy_splash import SplashRequest

from noval.DBHelper import DBHelper
from noval.items import NovalItem, BooksItem, ContentItem


class XlusirSpider(scrapy.Spider):
    name = 'xlusir_content'
    allowed_domains = ['m.xlusir.com', 'www.xlusir.com']
    start_urls = ['https://m.xlusir.com/']

    def parse(self, response):
        db = DBHelper()
        chapters = db.getChapterList()
        db.cursor.close()
        for item in chapters:
            yield SplashRequest(url=item['chapterUrl'], meta=item, callback=self.parsePageContent, args={'wait': 0.5})

    # 解析章节内容
    def parsePageContent(self, response):
        # item = response.meta
        content = []
        item = ContentItem()
        item['bookId'] = response.meta['bookId']
        item['chapterId'] = response.meta['chapterId']
        item['bookName'] = response.meta['bookName']
        item['chapterName'] = response.meta['chapterName']
        item['chapterUrl'] = response.meta['chapterUrl']
        textList = response.xpath("//div[@id='nr1']/text()").extract()
        for index, text in enumerate(textList):
            content.append(text)
        item['content'] = "".join(content)
        yield item

    # 解析info
    def parseBookInfo(self, info, index, xpath):
        return info.xpath(xpath).extract()[index]
