""" Scrubs scraped data of whitespaces and interesting characters and returns it into a data-maintenance friendly output. """

# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem

import re


class RentScraperPipeline(object):
    def process_item(self, item, spider):
        if item['price']:
            item['price'] = int(re.sub('[^\d.]+', '', ''.join(item['price'])))
        else:
            raise DropItem('Missing price in %s' % item)

        if item['bedrooms']:
            bedrooms, sqft = ''.join(item['bedrooms']).split('br')
            item['bedrooms'] = int(re.sub('[^\d.]+', '', bedrooms))
            item['sqft'] = re.sub('[^\d.]+', '', sqft)
                if item['sqft']:
                    item['sqft'] = int(item['sqft'])
        else:
            item['bedrooms'] = ''
            item['sqft'] = ''

        if item['neighborhood']:
            item['neighborhood'] = re.sub('[^\s\w.]+', '', ''.join(item['neighborhood'])).rstrip().lstrip()

        return item
