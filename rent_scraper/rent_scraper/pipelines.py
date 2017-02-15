# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
import re
import urllib
import geocoder
import json


class RentScraperPipeline(object):
    """ Scrubs scraped data of whitespaces and interesting characters and returns it as a data maintenance-friendly dictionary. """

    def process_item(self, item, spider):

        # Gets Craigslist posting ID
        if item['cl_id']:
            item['cl_id'] = re.split('\s', ''.join(item['cl_id']))[2]

        # Finds rental price; if none supplied or if it's listed below $50, drop item
        if item['price']:
            price = int(re.sub('[^\d.]+', '', ''.join(item['price'])))
            if price > 50:
                item['price'] = price
            else:
                raise DropItem('Missing price in %s' % item)
        else:
            raise DropItem('Missing price in %s' % item)

        # Finds bedrooms, bathrooms, and sqft, if provided
        if item['attributes']:
            attrs = item['attributes']

            for i, attribute in enumerate(attrs):
                if "BR" in attrs[i]:
                    item['bedrooms'] = int(''.join(re.findall('\d+', attrs[i])))
                if "Ba" in attrs[i]:
                    item['bathrooms'] = int(''.join(re.findall('\d+', attrs[i])))
                if "BR" not in attrs[i] and "Ba" not in attrs[i]:
                    item['sqft'] = int(attrs[i])

        # Get neighborhood name, if provided
        if item['neighborhood']:
            item['neighborhood'] = re.sub('[^\s\w/\.]+', '', ''.join(item['neighborhood'])).rstrip().lstrip()

        # Get posting date in UTC isoformat time
        if item['date']:
            item['date'] = ''.join(item['date'])

        # Find Google maps web address and convert to geolocation; if none exists drop record
        if item['location']:
            location_url = urllib.unquote(''.join(item['location'])).decode('utf8')
            location = location_url.split('loc:')[1]
            geo_location = geocoder.google(location)

            # If a geocoded location exists, get latitude and longitude, otherwise drop record
            if geo_location:
                item['latitude'] = geo_location.lat
                item['longitude'] = geo_location.lng
            else:
                raise DropItem('Missing location in %s' % item)

        else:
            raise DropItem('Missing location in %s' % item)

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


# class PostgresqlPipeline(object):
#     """ Writes data to PostgreSQL database. """

#     def load_rent_data():
#         for row in open('seed.jl'):
#             row = row.rstrip()

#             cl_id = row['cl_id']
#             price = row['price']
#             date = row['date']

#             rental = Rental(cl_id=cl_id,
#                             price=price,
#                             date=date_saved)

#             db.session.add(rental)

#         db.session.commit()


