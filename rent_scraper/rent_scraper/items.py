""" Defines the scraped items dictionary model. """

# -*- coding: utf-8 -*-

import scrapy


class CraigslistRental(scrapy.Item):
    cl_id = scrapy.Field()
    price = scrapy.Field()
    attributes = scrapy.Field()
    housing = scrapy.Field()
    sqft = scrapy.Field()
    neighborhood = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
