# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ZufangspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HouseItem(scrapy.Item):
    collection = table = 'house_info'
    title = Field()
    house_url = Field()
    location = Field()
    source = Field()
