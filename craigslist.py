# -*- coding: utf-8 -*-
import scrapy


class CraigslistSpider(scrapy.Spider):
    name = "craigslist"
    allowed_domains = ["https://sfbay.craigslist.org/search/sfc/apa"]
    start_urls = ['http://https://sfbay.craigslist.org/search/sfc/apa/']

    def parse(self, response):
        pass
