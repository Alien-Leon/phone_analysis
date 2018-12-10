import  scrapy
from ..items import Good
import requests


class GoodSpider(scrapy.Spider):
    name = 'good'

    def start_requests(self):
        urls = []
        keyword = '手机'
        begin = 0
        for self.page in range(1, 200, 2):
            begin += 60
            url = 'https://search.jd.com/Search?keyword=%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2' \
                  '&wq=%s&cid2=653&cid3=655&page=%s&s=%s&click=0' \
                  % (keyword, keyword, str(self.page), str(begin))
            urls.append(url)
        self.page = 1
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        response.body.decode(response.encoding).encode('utf-8')
        self.page += 2
        print('scraping page', str(self.page))

        for good, id in zip(response.css('.gl-item'), response.css('.gl-item::attr(data-pid)')):
            d = {
                'id': id.extract(),
                'name': good.css('.p-name em::text').extract_first(),
                'price': good.css('.p-price i::text').extract_first(),
                'href': good.css('.p-img a::attr(href)').extract_first(),
                'img': good.css('.p-img img::attr(source-data-lazy-img)').extract_first(),
                'comment_count': good.css('.p-commit strong a::text').extract_first(),
                'shop': good.css('.p-shop a::attr(title)').extract_first(),
            }
            if d['href'].find('ccc-x.jd.com'):
                if d['href'].startswith('//'):
                    d['href'] = 'https:' + d['href']
                d['href'] = requests.get(d['href']).url
            # for k,v  in d.items():
            #     print(k, v)
            yield Good(d)