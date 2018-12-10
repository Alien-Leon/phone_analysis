import scrapy
import csv
import json

class CommentSpider(scrapy.Spider):
    name = 'comment'
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
        comment_count = self.comment_counts[self.cur_good]
        good_id = self.goods_id[self.cur_good]
        self.cur_good += 1
        # 每个商品最多抓取1w条评论
        if comment_count.find('万') > 0:
            comment_count = 10000
        else:
            if comment_count.endswith('+'):
                comment_count = int(comment_count[:-1])
            else:
                comment_count = int(comment_count)


        for page in range(1, int(comment_count / 10) + 1):
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv12887' \
                  '&productId=%s&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&rid=0&fold=1'\
                  % (good_id, str(page))
            urls.append(url)

        print('scraping good', good_id)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        s = response.body_as_unicode()
        begin = s.find('{')
        end = s.rfind('}') + 1
        # print(s[begin:end])
        js = json.loads(s[begin:end])
        for comment in js['comment']:

            content = comment['content']
            date = comment['creationTime']
            reference_name = comment['referenceName']  # 购买的商品名称
            score = comment['score']
            province = comment['userProvince']
            content += comment['afterUserComment']['hAfterUserComment']['content'] # 添加追评
            user_level_name = comment['userLevelName']
            user_level_id = comment['userLevelId']
            recommend = comment['recommend']
        for hot_comment in js['hotCommentTagStatistics']:
            hot_comment_count = hot_comment['count']
            hot_comment_name = hot_comment['name']

        # print(js)