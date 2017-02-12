# -*- coding: utf-8 -*-
from scrapy.spiders import Spider, Request
from scrapy_craigslist.items import CraigslistRental


class CraigslistSpider(Spider):
    """ A spider built for Craigslist that will extract the URL page extension, price, bedrooms, neighborhood, and date of each rental posting on the start_url and subsequent pages. """
    name = 'craigslist'

    allowed_domains = ['https://craigslist.org']
    start_urls = ['https://sfbay.craigslist.org/search/sfc/apa']


    def parse(self, response):
        item = CraigslistRental()

        rentals = response.xpath('//li[contains(@class,"result-row")]')

        for rental in rentals:
            item['cl_id'] = rental.xpath('a[contains(@href,"/sfc")]/@href').extract()
            item['price'] = rental.xpath('a/span/text()').extract()
            item['bedrooms'] = rental.xpath('p/span/span[contains(@class, "housing")]/text()').extract()
            item['neighborhood'] = rental.xpath('p/span/span[contains(@class, "result-hood")]/text()').extract()
            item['date'] = rental.xpath('p/time/@datetime').extract()

            yield item

        # Follows subsequent listing pages
        next_page = response.xpath('//a[contains(@class, "button next")]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse)
