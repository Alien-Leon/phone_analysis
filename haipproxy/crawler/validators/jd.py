from config.settings import (
    TEMP_JD_QUEUE, VALIDATED_JD_QUEUE,
    TTL_JD_QUEUE, SPEED_JD_QUEUE)
# ValidatorRedisSpider提供了分布式父类爬虫
from ..redis_spiders import ValidatorRedisSpider
# BaseValidator提供了基本的请求错误处理，但是业务相关逻辑错误需要自己实现
from .base import BaseValidator

class JDValidator(BaseValidator, ValidatorRedisSpider):
    # scrapy爬虫名，必须设置且不能与已知的重复
    name = 'jd'
    # 需要验证的URL，建议选择一个稳定且有代表意义的url，数据结构是一个list
    urls = [
        'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv12887&productId=100000287113&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1'
    ]
    # 下面四个属性必须设置，并且与maps中的一致
    task_queue = TEMP_JD_QUEUE
    score_queue = VALIDATED_JD_QUEUE
    ttl_queue = TTL_JD_QUEUE
    speed_queue = SPEED_JD_QUEUE
    # 判断success_key是否在响应内容中，从而判断IP是否正常，默认为''，表示正常
    success_key = 'fetchJSON'