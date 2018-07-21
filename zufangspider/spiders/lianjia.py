# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, signals, Request
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher

from zufangspider.items import HouseItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['cd.lianjia.com']
    start_url = 'https://cd.lianjia.com/zufang/pg{page}'

    # def __init__(self):  # 初始化
    #     self.browser = webdriver.Chrome()  # 创建谷歌浏览器对象
    #     super(LianjiaSpider, self).__init__()  # 设置可以获取上一级父类基类的，__init__方法里的对象封装值
    #     # dispatcher.connect()信号分发器，第一个参数信号触发函数，
    #     # 第二个参数是触发信号，signals.spider_closed是爬虫结束信号
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    #     # 运行到此处时，就会去中间件执行，RequestsChrometmiddware中间件了
    #
    # def spider_closed(self, spider):  # 信号触发函数
    #     print('爬虫结束 停止爬虫')
    #     self.browser.quit()

    def start_requests(self):
        for i in range(1, 101):
            url = self.start_url.format(page=i)
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        result = Selector(response)
        result_lis = result.xpath('//*[@id="house-lst"]/li')
        for li in result_lis:
            item = HouseItem()
            item['title'] = li.xpath('./div[2]/h2/a/text()').extract_first()
            item['house_url'] = li.xpath('./div[2]/h2/a/@href').extract_first()
            location = li.xpath('./div[2]/div[1]/div[1]/a/span/text()').extract_first()
            item['location'] = location.strip()
            item['source'] = '链家租房'
            yield item

