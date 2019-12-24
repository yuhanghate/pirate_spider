# -*- coding: utf-8 -*-
import scrapy

from noval.items import NovalItem, BooksItem


class XlusirSpider(scrapy.Spider):
    name = 'xlusir'
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
    # 章节列表名称
    BOOK_CHAPTER_LIST_TITLE = "//div[@id='list']/dl/dd/a/text()"
    # 章节
    BOOK_CHAPTER_LIST_URL = "//div[@id='list']/dl/dd/a/@href"

    def parse(self, response):
        for i in range(1, 337):
            url = self.start_urls[0] + "xiaoshuodaquan/page_%s.html" % i
            yield scrapy.Request(url=url, callback=self.parsePage)

    # 解析小说列表
    def parsePage(self, response):
        list = response.xpath("//div[@class='bookinfo']")
        for index, info in enumerate(list):
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
            # yield scrapy.Request(url=item['bookUrl'], meta=item,
            #                      callback=self.parsePageChapter)

    # 解析章节列表
    def parsePageChapter(self, response):
        item = response.meta
        chapterList = response.xpath("//div[@id='list']/dl/dd")

        # 目录章节大于10的,当连载
        if (len(chapterList) > 10):
            return None

        for index, chapter in enumerate(chapterList):
            chapterName = self.parseBookInfo(info=chapter, index=index, xpath=self.BOOK_CHAPTER_LIST_TITLE)
            chapterUrl = self.parseBookInfo(info=chapter, index=index, xpath=self.BOOK_CHAPTER_LIST_URL)

            item['chapterName'] = chapterName
            item['chapterUrl'] = "https://m.xlusir.com%s" % chapterUrl
            yield item
            # yield SplashRequest(url=item['chapterUrl'], meta=item, callback=self.parsePageContent, args={'wait': 0.5})

    # 解析章节内容
    def parsePageContent(self, response):
        item = response.meta
        content = ""
        textList = response.xpath("//div[@id='nr1']/text()").extract()
        for index, text in enumerate(textList):
            content += text
        item['content'] = content
        yield item

    # 解析info
    def parseBookInfo(self, info, index, xpath):
        return info.xpath(xpath).extract()[index]
