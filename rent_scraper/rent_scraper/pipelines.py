# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
import re
import json

# from rent_utilities import *


class RentScraperPipeline(object):
    """ Scrubs scraped data of whitespaces and interesting characters and returns it into a data-maintenance friendly output. """
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
            item['neighborhood'] = re.sub('[^\s\w/\.]+', '', ''.join(item['neighborhood'])).rstrip().lstrip()

        if item['cl_id']:
            item['cl_id'] = ''.join(item['cl_id'])

        if item['date']:
            item['date'] = ''.join(item['cl_id'])

        return item


class JsonWriterPipeline(object):
    """ Takes scrubbed data and outputs as JSON file. """
    def open_spider(self, spider):
        self.file = open('seed.jl', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item


class WriteToDbPipeline(object):
    """ Writes data to database. """
    pass
