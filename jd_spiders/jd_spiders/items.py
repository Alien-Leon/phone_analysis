# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdSpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Good(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    comment_count = scrapy.Field()
    img = scrapy.Field()
    href = scrapy.Field()
    shop = scrapy.Field()

class Comment(scrapy.Item):
    id = scrapy.Field()
    user_province = scrapy.Field()  # 评论用户来自的地区
    content = scrapy.Field()  # 评论内容
    good_id = scrapy.Field()  # 评论的商品ID
    good_name = scrapy.Field()  # 评论的商品名字
    date = scrapy.Field()  # 评论时间
    score = scrapy.Field()  # 评分
    recommend = scrapy.Field()
    user_level_name = scrapy.Field()  # 银牌会员，钻石会员等
    user_level_id = scrapy.Field()


# 标识某个商品对应的热评标签
class HotComment(scrapy.Item):
    id = scrapy.Field()     # 标识对应的商品id
    comment_dict = scrapy.Field()   # 存储对应的热评标签字符串
