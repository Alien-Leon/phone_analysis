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
    user_name = scrapy.Field()  # 评论用户的名字
    user_id = scrapy.Field()  # 评论用户的ID
    userProvince = scrapy.Field()  # 评论用户来自的地区
    content = scrapy.Field()  # 评论内容
    good_id = scrapy.Field()  # 评论的商品ID
    good_name = scrapy.Field()  # 评论的商品名字
    date = scrapy.Field()  # 评论时间
    replyCount = scrapy.Field()  # 回复数
    score = scrapy.Field()  # 评分
    status = scrapy.Field()  # 状态
    title = scrapy.Field()
    userLevelId = scrapy.Field()
    userRegisterTime = scrapy.Field()  # 用户注册时间
    productColor = scrapy.Field()  # 商品颜色
    productSize = scrapy.Field()  # 商品大小
    userLevelName = scrapy.Field()  # 银牌会员，钻石会员等
    userClientShow = scrapy.Field()  # 来自什么 比如来自京东客户端
    isMobile = scrapy.Field()  # 是否来自手机
    days = scrapy.Field()  # 天数
    commentTags = scrapy.Field()  # 标签

# 标识某个商品对应的热评标签
class HotComment(scrapy.Item):
    good_ID = scrapy.Field()
    name = scrapy.Field()
    count = scrapy.Field()