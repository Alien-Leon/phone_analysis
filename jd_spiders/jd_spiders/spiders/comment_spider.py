import scrapy
import csv
import json
from ..items import Comment, HotComment
from json import JSONDecodeError

class CommentSpider(scrapy.Spider):
    name = 'comment'
    goods_id = []
    comment_counts = []
    with open('goods.csv', 'r') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            goods_id.append(row['id'])
            comment_counts.append(row['comment_count'])
    error_url = {}

    def start_requests(self):
        # 每个商品最多显示100页，即最多只能加载1000条评论
        for good_id, comment_count in zip(self.goods_id, self.comment_counts):
            if comment_count.find('万') > 0:
                comment_count = 1000
            else:
                if comment_count.endswith('+'):
                    comment_count = int(comment_count[:-1])
                else:
                    comment_count = int(comment_count)

            comment_count /= 10

            comment_count += 1

            page_count = int(comment_count) if comment_count < 100 else 100

            for page in range(1, page_count):
                url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv12887' \
                      '&productId=%s&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&rid=0&fold=1'\
                      % (good_id, str(page))
                print('scraping good', good_id, 'comment-count:', comment_count, 'page:', str(page))
                yield scrapy.Request(url=url, callback=self.parse)
        # url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv2671&productId=100000727104&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        # yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        s = response.body_as_unicode()

        begin = s.find('{')
        end = s.rfind('}') + 1
        # print('js:', s[begin:end])
        try:
            js = json.loads(s[begin:end])
            for comment in js['comments']:
                d = {
                    'id' : comment['id'],
                    'user_province': comment['userProvince'],

                    'content': comment['content'] , # 添加追评,
                    'good_id': comment['referenceId'],
                    'good_name': comment['referenceName'],  # 购买的商品名称
                    'date': comment['creationTime'],
                    'score': comment['score'],
                    'recommend': comment['recommend'],
                    'user_level_name': comment['userLevelName'],
                    'user_level_id': comment['userLevelId'],
                }
                if comment.get('afterUserComment', None):
                    d['content'] += comment['afterUserComment']['hAfterUserComment']['content']
                yield Comment(d)
        except JSONDecodeError:
            print('retry request', response.url)
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)



class HotCommentSpider(scrapy.Spider):
    name = 'hot_comment'
    cur_good = 0
    goods_id = []
    comment_counts = []
    with open('goods.csv') as f:
        f_csv = csv.DictReader(f)
        for row in f_csv:
            goods_id.append(row['id'])
            comment_counts.append(row['comment_count'])

    def start_requests(self):
        urls = []

        # 访问第一页评论以获得热评标签
        for good_id in self.goods_id:
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv12887' \
                  '&productId=%s&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&rid=0&fold=1' \
                  % (good_id, '1')
            urls.append(url)
            # print('scraping good', good_id)
        for url in urls:
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        s = response.body_as_unicode()
        # print(s)
        begin = s.find('{')
        end = s.rfind('}') + 1
        # print(s[begin:end])
        js = json.loads(s[begin:end])
        comment_dict = {}
        for hot_comment in js['hotCommentTagStatistics']:
            comment_dict[hot_comment['name']] = hot_comment['count']

        self.cur_good += 1
        print(str(comment_dict))
        yield HotComment({
            'id': self.goods_id[self.cur_good],
            'comment_dict': str(comment_dict)
        })