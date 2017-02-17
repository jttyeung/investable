""" Defines the scraped items dictionary model of items = {}. """

# -*- coding: utf-8 -*-

import scrapy


class CraigslistRental(scrapy.Item):

    # Dictionary keys created for scraping in craigslist.py
    cl_id = scrapy.Field()
    price = scrapy.Field()
    attributes = scrapy.Field()
    housing = scrapy.Field()
    neighborhood = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()

    # Additional dictionary keys created upon data cleanse in pipelines.py
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    sqft = scrapy.Field()
    latlng = scrapy.Field()
