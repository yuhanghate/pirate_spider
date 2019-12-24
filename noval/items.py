# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NovalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    bookName = scrapy.Field()
    author = scrapy.Field()
    lastChapter = scrapy.Field()
    description = scrapy.Field()
    pageUrl = scrapy.Field()
    bookUrl = scrapy.Field()
    chapterName = scrapy.Field()
    chapterUrl = scrapy.Field()
    content = scrapy.Field()
    pass


# 书本信息
class BooksItem(scrapy.Item):
    bookName = scrapy.Field()
    author = scrapy.Field()
    lastChapter = scrapy.Field()
    description = scrapy.Field()
    pageUrl = scrapy.Field()
    bookUrl = scrapy.Field()
    pass

# 没有章节的书籍或者超过100章的书箱
class BooksDeleteItem(scrapy.Item):
    deleteFlag = scrapy.Field()
    bookId = scrapy.Field()
    pass


# 章节
class ChapterItem(scrapy.Item):
    bookId = scrapy.Field()
    bookName = scrapy.Field()
    author = scrapy.Field()
    chapterName = scrapy.Field()
    chapterUrl = scrapy.Field()
    index = scrapy.Field()
    pass


# 内容
class ContentItem(scrapy.Item):
    bookId = scrapy.Field()
    chapterId = scrapy.Field()
    bookName = scrapy.Field()
    chapterName = scrapy.Field()
    chapterUrl = scrapy.Field()
    content = scrapy.Field()
    pass
