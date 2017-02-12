""" Defines the scraped items dictionary model. """

# -*- coding: utf-8 -*-

import scrapy


class CraigslistRental(scrapy.Item):
    cl_id = scrapy.Field()
    price = scrapy.Field()
    bedrooms = scrapy.Field()
    neighborhood = scrapy.Field()
    date = scrapy.Field()
