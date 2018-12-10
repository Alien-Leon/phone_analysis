# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JdSpidersPipeline(object):
    def process_item(self, item, spider):
        return item

import csv

class GoodPipeline(object):
    # 此处字段名与items.py中设置保持一致
    header = ['id', 'name', 'price', 'comment_count', 'img', 'href', 'shop']

    def open_spider(self, spider):
        if spider.name == 'good':
            # 在爬虫启动时，创建csv，并设置newline=''来避免空行出现
            print('open csv')
            self.file = open('goods.csv','w',newline='')
            # 启动csv的字典写入方法
            self.writer = csv.DictWriter(self.file, self.header)
            # 写入字段名称作为首行
            self.writer.writeheader()

    def close_spider(self, spider):
        # 在爬虫结束时，关闭文件节省资源
        self.file.close()

    def process_item(self, item, spider):
        if spider.name == 'good':
            # 把每次输出的item，写入csv中
            self.writer.writerow(item)
            return item