# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider, Spider, Request, Rule
from scrapy.linkextractors import LinkExtractor
from rent_scraper.items import CraigslistRental


class CraigslistSpider(CrawlSpider):
    """ A spider built for Craigslist that will extract the URL page extension, price, bedrooms, neighborhood, and date of each rental posting on the start_url and subsequent pages. """

    # Spider name
    name = 'craigslist'

    # Start crawling from these URLs
    start_urls = ['https://sfbay.craigslist.org/search/sfc/apa']

    # Extracts links out of the start URL with the class restriction specified (refers to the rental posting link)
    # Follows the links, returning the response to the callback function
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="result-title hdrlnk"]')), follow=True, callback='parse_item'),
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@class, "button next")]')), follow=True, callback='parse_item'),
    )

    def parse_item(self, response):
        """
        Parses each posting for any of the following rental details available and creates dictionary items of each posting:
            - Posting ID (cl_id)
            - Price
            - Beds / Baths (attributes)
            - Sqft (housing)
            - Neighborhood
            - Date Posted
            - Google Maps Location
        """

        item = CraigslistRental()

        item['cl_id'] = response.xpath('//div/p[@class="postinginfo"]/text()').extract()
        item['price'] = response.xpath('//span/span[contains(@class, "price")]/text()').extract()
        item['attributes'] = response.xpath('//p[contains(@class, "attrgroup")]/span/b/text()').extract()
        item['housing'] = response.xpath('//span/span[contains(@class, "housing")]/text()').extract()
        item['neighborhood'] = response.xpath('//span/small/text()').extract()
        item['date'] = response.xpath('//time[contains(@class, "timeago")]/@datetime').extract_first()
        item['location'] = response.xpath('//a[contains(@href, "https://maps.google.com/")]/@href').extract()

        yield item
