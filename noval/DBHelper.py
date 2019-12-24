import datetime

import pymysql
from scrapy.utils.project import get_project_settings  # 导入seetings配置


class DBHelper:
    """这个类也是读取settings中的配置，自行修改代码进行操作"""

    def __init__(self):
        settings = get_project_settings()  # 获取settings配置，设置需要的信息

        self.connect = pymysql.connect(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()


    # 插入数据书本
    def insertBooks(self, item):
        query = '''SELECT book_name FROM sex_books WHERE book_name = %s AND author = %s LIMIT 1'''
        insert = '''insert into sex_books(book_name,author,description,last_chapter_name,book_url,page_url, create_at) values(%s,%s,%s,%s,%s,%s,%s)'''
        try:
            self.cursor.execute(query, (item['bookName'], item['author']))
            book = self.cursor.fetchone()
            if not book:
                dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                value = (
                    item['bookName'],
                    item['author'],
                    item['description'],
                    item['lastChapter'],
                    item['bookUrl'],
                    item['pageUrl'],
                    dt,
                )
                self.cursor.execute(insert, value)
                self.connect.commit()
        except Exception as eror:
            print(eror)
        return item

    # 插入章节
    def insertChapters(self, item):
        query = ''' SELECT book_id FROM sex_book_chapter WHERE book_id = %s AND chapter_url = %s '''
        insert = ''' INSERT INTO sex_book_chapter(book_id, book_name, author, chapter_name, chapter_url, chapter_index, create_time) VALUES(%s, %s, %s, %s, %s, %s, %s) '''
        bookId = item['bookId']
        bookName = item['bookName']
        chapterName = item['chapterName']
        chapterUrl = item['chapterUrl']
        author = item['author']
        index = item['index']
        createTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute(query, (bookId, chapterUrl))
            chapter = self.cursor.fetchone()
            if not chapter:
                value = (bookId, bookName, author, chapterName, chapterUrl, index, createTime)
                self.cursor.execute(insert, value)
                self.connect.commit()
        except Exception as eror:
            print(eror)
        return item

    # 插入内容
    def insertContent(self, item):
        query = '''SELECT id FROM sex_book_content WHERE book_id = %s AND chapter_id = %s'''
        insert = ''' INSERT INTO sex_book_content(book_id, chapter_id, book_name, chapter_name, chapter_url, content, create_time) 
        VALUES(%s, %s, %s, %s, %s, %s, %s)'''
        bookId = item['bookId']
        chapterId = item['chapterId']
        bookName = item['bookName']
        chapterName = item['chapterName']
        chapterUrl = item['chapterUrl']
        content = item['content']
        createTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.cursor.execute(query, (bookId, chapterUrl))
            chapter = self.cursor.fetchone()
            if not chapter:
                value = (bookId, chapterId, bookName, chapterName, chapterUrl, content, createTime)
                self.cursor.execute(insert, value)
                self.connect.commit()
        except Exception as eror:
            print(eror)

    # 更新删除状态
    def updateDeleteFlagByBooks(self, item):
        update = '''UPDATE  sex_books SET delete_flag = 1 WHERE id = %s'''
        bookId = item['bookId']
        try:
            self.cursor.execute(update, bookId)
            self.connect.commit()
        except Exception as eror:
            print(eror)

    # 获取所有书列表
    def getBooksList(self):
        query = 'SELECT id, book_name, author, book_url FROM sex_books WHERE delete_flag = 0'
        urls = []
        try:
            self.cursor.execute(query, ())
            book = self.cursor.fetchall()

            for id, book_name, author, book_url in book:
                urls.append({"id": id, "bookName": book_name, "author": author, "bookUrl": book_url})

        except Exception as error:
            print("")
        return urls

    # 获取内容
    def getChapterList(self):
        query = 'SELECT id, chapter_name, chapter_url, book_id, book_name FROM sex_book_chapter'
        items = []
        try:
            self.cursor.execute(query)
            content = self.cursor.fetchall()

            for id, chapter_name, chapter_url, book_id, book_name in content:
                items.append({"chapterId": id, "bookId": book_id, "bookName": book_name, "chapterName": chapter_name,
                              "chapterUrl": chapter_url})
        except Exception as error:
            print("")
        return items
