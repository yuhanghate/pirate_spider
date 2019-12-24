# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from noval.DBHelper import DBHelper
from noval.items import NovalItem, BooksItem, ChapterItem, BooksDeleteItem


class XlusirSpider(scrapy.Spider):
    name = 'xlusir_chapter'
    allowed_domains = ['m.xlusir.com', 'www.xlusir.com']

    # 增加更新
    # 获取数据库所有书本URL

    start_urls = ['https://m.xlusir.com/']

    # 章节列表名称
    BOOK_CHAPTER_LIST_TITLE = "//div[@id='list']/dl/dd/a/text()"
    # 章节
    BOOK_CHAPTER_LIST_URL = "//div[@id='list']/dl/dd/a/@href"

    def parse(self, response):
        db = DBHelper()
        books = db.getBooksList()
        db.cursor.close()
        for item in books:
            yield SplashRequest(url=item['bookUrl'], meta=item, callback=self.parsePageChapter, args={'wait': 0.5})

    # 解析章节列表
    def parsePageChapter(self, response):
        bookName = response.meta['bookName']
        bookId = response.meta['id']
        author = response.meta['author']
        item = ChapterItem()
        deleteFlagItem = BooksDeleteItem()
        deleteFlagItem['deleteFlag'] = 1
        deleteFlagItem['bookId'] = bookId
        chapterList = response.xpath("//div[@id='list']/dl/dd")

        # 目录章节大于100的或没章节的.书籍标志删除
        if len(chapterList) > 100 or len(chapterList) == 0:
            yield deleteFlagItem
        else:
            for index, chapter in enumerate(chapterList):
                chapterName = self.parseBookInfo(info=chapter, index=index, xpath=self.BOOK_CHAPTER_LIST_TITLE)
                chapterUrl = self.parseBookInfo(info=chapter, index=index, xpath=self.BOOK_CHAPTER_LIST_URL)

                item['bookId'] = bookId
                item['bookName'] = bookName
                item['author'] = author
                item['chapterName'] = chapterName
                item['chapterUrl'] = "https://m.xlusir.com%s" % chapterUrl
                item['index'] = index
                yield item


    # 解析info
    def parseBookInfo(self, info, index, xpath):
        return info.xpath(xpath).extract()[index]
