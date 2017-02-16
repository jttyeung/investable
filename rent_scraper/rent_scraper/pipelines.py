# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem
import re
import urllib
import geocoder
import json

import model


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


# class JsonWriterPipeline(object):
#     """ Takes scrubbed data and outputs as JSON Lines file. Only used for creating a seed file for test database. """

#     def open_spider(self, spider):
#         self.file = open('seed.jl', 'wb')

#     def close_spider(self, spider):
#         self.file.close()

#     def process_item(self, item, spider):
#         line = json.dumps(dict(item)) + '\n'
#         self.file.write(line)
#         return item


class PostgresqlPipeline(object):
    """ Writes data to PostgreSQL database. """

    def load_data_from_scraper():
        """ Method used to write data to database directly from the scraper pipeline. """

#         for rental in item:

#             cl_id = rental['cl_id']
#             price = rental['price']
#             date = rental['date']
#             neighborhood = rental['neighborhood']
#             bedrooms = rental['bedrooms']
#             bathrooms = rental['bathrooms']
#             sqft = rental['sqft']
#             latitude = rental['latitude']
#             longitude = rental['longitude']

#             # Add rental details to UnitDetails table
#             rental_details = UnitDetails(
#                                 neighborhood=neighborhood,
#                                 bedrooms=bedrooms,
#                                 bathrooms=bathrooms,
#                                 sqft=sqft,
#                                 latitude=latitude,
#                                 longitude=longitude
#                             )

#             db.session.add(rental_details)

#             # Add rental unit to Rentals table
#             rental = Rental(
#                         cl_id=cl_id,
#                         price=price,
#                         date=date_posted
#                     )

#             db.session.add(rental)
# """
# should i be committing after each added set of tables? (before instead of after the for loop)
# why is this lined up so ugly

# """
#         db.session.commit()


    def load_seed_file():
        """ Method used to write JSON Lines file data to database, if necessary. Should prioritize use of load_data_from_scraper method instead for direct data handling. """

        for row in open('seed.jl'):
            row = row.rstrip()

            cl_id = row['cl_id']
            price = row['price']
            date = row['date']
            neighborhood = row['neighborhood']
            bedrooms = row['bedrooms']
            bathrooms = row['bathrooms']
            sqft = row['sqft']
            latitude = row['latitude']
            longitude = row['longitude']

            # Add rental details to UnitDetails table
            rental_details = UnitDetails(
                                neighborhood=neighborhood,
                                bedrooms=bedrooms,
                                bathrooms=bathrooms,
                                sqft=sqft,
                                latitude=latitude,
                                longitude=longitude
                            )

            db.session.add(rental_details)

            # Add rental unit to Rentals table
            rental = Rental(
                        cl_id=cl_id,
                        price=price,
                        date=date_posted
                    )

            db.session.add(rental)

        db.session.commit()
