# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JijiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    phone_number = scrapy.Field()
    customer_type = scrapy.Field()
    isRegister = scrapy.Field()
