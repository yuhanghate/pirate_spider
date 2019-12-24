# -*- coding: utf-8 -*-
import scrapy

from noval.items import NovalItem, BooksItem


class XlusirSpider(scrapy.Spider):
    name = 'xlusir_book'
    allowed_domains = ['m.xlusir.com', 'www.xlusir.com']
    start_urls = ['https://m.xlusir.com/']

    # 书名
    BOOK_NAME = "//h4[@class='bookname']/*/a/@title"
    # 书本地址
    BOOK_CHPATER_URL = "//h4[@class='bookname']/*/a/@href"
    # 作者
    AUTHOR = "//div[@class='author']/a/@title"
    # 最后章节
    LAST_CHAPTER = "//div[@class='update']/a/text()"
    # 简介
    DESCRIPTION = "//div[@class='intro_line']/text()"

    def parse(self, response):
        for i in range(1, 337):
            url = self.start_urls[0] + "xiaoshuodaquan/page_%s.html" % i
            yield scrapy.Request(url=url, callback=self.parsePage)

    # 解析小说列表
    def parsePage(self, response):
        infos = response.xpath("//div[@class='bookinfo']")
        for index, info in enumerate(infos):
            bookName = self.parseBookInfo(info=info, index=index, xpath=self.BOOK_NAME)
            bookChapterUrl = self.parseBookInfo(info=info, index=index, xpath=self.BOOK_CHPATER_URL)
            author = self.parseBookInfo(info=info, index=index, xpath=self.AUTHOR)
            lastChapter = self.parseBookInfo(info=info, index=index, xpath=self.LAST_CHAPTER)
            description = self.parseBookInfo(info=info, index=index, xpath=self.DESCRIPTION)

            item = BooksItem()
            item['bookName'] = bookName
            item['author'] = author.replace("作    者：", "")
            item['lastChapter'] = lastChapter
            item['description'] = description
            item['pageUrl'] = response.url
            item['bookUrl'] = "https://www.xlusir.com%s" % bookChapterUrl

            yield item

    # 解析info
    def parseBookInfo(self, info, index, xpath):
        return info.xpath(xpath).extract()[index]
