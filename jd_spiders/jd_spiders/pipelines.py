# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JdSpidersPipeline(object):
    def process_item(self, item, spider):
        return item

import csv
import pymysql
from . import settings
from .items import Comment
from . import server_config

class GoodPipeline(object):
    # 此处字段名与items.py中设置保持一致
    good_header = ['id', 'name', 'price', 'comment_count', 'img', 'href', 'shop']
    hot_comment_header = ['id', 'comment_dict']

    def open_spider(self, spider):
        if spider.name == 'good':
            # 在爬虫启动时，创建csv，并设置newline=''来避免空行出现
            print('open csv')
            self.file = open('goods.csv','w',newline='')
            # 启动csv的字典写入方法
            self.writer = csv.DictWriter(self.file, self.good_header)
            # 写入字段名称作为首行
            self.writer.writeheader()
        elif spider.name == 'hot_comment':
            print('open csv')
            self.file = open('hot_comment.csv', 'w', newline='')
            # 启动csv的字典写入方法
            self.writer = csv.DictWriter(self.file, self.hot_comment_header)
            # 写入字段名称作为首行
            self.writer.writeheader()

    def close_spider(self, spider):
        # 在爬虫结束时，关闭文件节省资源
        if spider.name == 'good' or spider.name == 'hot_comment':
            self.file.close()

    def process_item(self, item, spider):

        # 把每次输出的item，写入csv中
        if spider.name == 'good' or spider.name == 'hot_comment':
            self.writer.writerow(item)
            return item


class CommentPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=server_config.MYSQL_HOST,
            db=server_config.MYSQL_DBNAME,
            user=server_config.MYSQL_USER,
            passwd=server_config.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == Comment:
            try:
                self.cursor.execute("""select * from jd_comment where id = %s""", item["id"])
                ret = self.cursor.fetchone()
                # 更新部分未成功爬取入库的数据
                if not ret:
                    self.cursor.execute(
                        """insert into jd_comment(id, user_province, content, good_id, good_name, date
                        ,score, user_level_name, user_level_id, recommend)
                          value (%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)""",
                        (item['id'],
                         item['user_province'],
                         item['content'],
                         item['good_id'],
                         item['good_name'],
                         item['date'],
                         item['score'],
                         item['user_level_name'],
                         item['user_level_id'],
                         item['recommend']))
                self.connect.commit()
                # print('save success', str(item))
            except Exception as error:
                print(error)
            return item
