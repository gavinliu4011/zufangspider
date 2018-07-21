# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging

import requests
from fake_useragent import UserAgent
from scrapy.http import HtmlResponse


class RequestsChrometmiddware(object):  # 浏览器访问中间件

    def process_request(self, request, spider):  # 重写process_request请求方法
        if spider.name == 'lvmama':  # 判断爬虫名称为pach时执行
            spider.browser.get(request.url)  # 用谷歌浏览器访问url
            import time
            time.sleep(3)
            print('访问：{0}'.format(request.url))  # 打印访问网址
            # 设置响应信息，由浏览器响应信息返回
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding='utf-8',
                                request=request)


class ProxyMiddleware(object):
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        # if request.meta.get('retry_times'):
        # proxy = self.get_random_proxy()
        proxy = '101.236.60.52:8866'
        if proxy:
            uri = 'https://{proxy}'.format(proxy=proxy)
            self.logger.debug('使用代理 ' + proxy)
            request.meta['proxy'] = uri

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )


class RandomUserAgentMiddleware(object):  # 自定义浏览器代理中间件
    # 随机更换Requests请求头信息的User-Agent浏览器用户代理
    def __init__(self, crawler):
        # 获取上一级父类基类的，__init__方法里的对象封装值
        super(RandomUserAgentMiddleware, self).__init__()
        # 实例化浏览器用户代理模块类
        self.ua = UserAgent()
        # 获取settings.py配置文件里的RANDOM_UA_TYPE配置的浏览器类型，
        # 如果没有，默认random，随机获取各种浏览器类型
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod  # 函数上面用上装饰符@classmethod，函数里有一个必写形式参数cls用来接收当前类名称
    def from_crawler(cls, crawler):  # 重载from_crawler方法
        return cls(crawler)  # 将crawler爬虫返回给类

    def process_request(self, request, spider):  # 重载process_request方法
        def get_ua():  # 自定义函数，返回浏览器代理对象里指定类型的浏览器信息
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())  # 将浏览器代理信息添加到Requests请求
