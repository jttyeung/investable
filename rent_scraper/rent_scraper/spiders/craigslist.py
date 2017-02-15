# -*- coding: utf-8 -*-

from scrapy.spiders import Spider, Request
from rent_scraper.items import CraigslistRental


class CraigslistSpider(CrawlSpider):
    """ A spider built for Craigslist that will extract the URL page extension, price, bedrooms, neighborhood, and date of each rental posting on the start_url and subsequent pages. """

    # Spider name
    name = 'craigslist'

    # Restricts crawler to domain
    allowed_domains = ['https://craigslist.org']


    def start_requests(self):
        """ Creates a starting request for initial search page(s). """

        urls = ['https://sfbay.craigslist.org/search/sfc/apa']

        for url in urls:
            yield Request(url=url, callback=self.get_rental_links)


    def get_rental_links(self, response):
        """ Extracts Craigslist links for each rental posting from from the initial search, creates a URL request, and adds them to the data parsing queue. """

        rentals = response.xpath('//li[contains(@class,"result-row")]')

        for rental in rentals:
            rental_partial_url = rental.xpath('a[contains(@href,"/sfc")]/@href').extract_first()
            rental_full_url = response.urljoin(rental_partial_url)

            print {'url': rental_full_url}

            if rental_full_url is not None:
                yield Request(url=rental_full_url, callback=self.parse)


    def parse(self, response):
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
        print '-------------------------------------'
        item = CraigslistRental()

        item['cl_id'] = response.xpath('//div/p[@class="postinginfo"]/text()').extract()
        item['price'] = response.xpath('//span/span[contains(@class, "price")]/text()').extract()
        item['attributes'] = response.xpath('//p[contains(@class, "attrgroup")]/span/b/text()').extract()
        item['housing'] = response.xpath('//span/span[contains(@class, "housing")]/text()').extract()
        item['neighborhood'] = response.xpath('//span/small/text()').extract()
        item['date'] = response.xpath('//time[contains(@class, "timeago")]/@datetime').extract_first()
        item['location'] = response.xpath('//a[contains(@href, "https://maps.google.com/")]/@href').extract()

        print item


        # Follows subsequent listing pages
        # next_page = response.xpath('//a[contains(@class, "button next")]/@href').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield Request(next_page, callback=self.parse)
