from flask import json


def get_rent_averages():
    """ Reads JSON Lines file of scraped and scrubbed rental information. """

    file = open('seed.jl').readlines()
    json_file = json.loads(file)

    for line in json_file:
        price = line['price']
        neighborhood = line['neighborhood']
        bedrooms = line['bedrooms']
        sqft = line['sqft']
        date = line['date']

        rent_by_neighborhood = {}
        # rent_by_neighborhood['neighborhood']: { units: , total_rent: }

        # neighborhood
        if rent_by_neighborhood[neighborhood]:
            rent_by_neighborhood[neighborhood]['units'] = rent_by_neighborhood[neighborhood].get(units, 0) + 1
            rent_by_neighborhood[neighborhood]['total_price'] = rent_by_neighborhood.get(total_price, 0) + total_price
        else:
            rent_by_neighborhood[neighborhood]['units'] = units
            rent_by_neighborhood[neighborhood]['total_price'] = price


        def calculate_rent_by_neighborhood():
            """ Gets rent average by neighborhood. """

            return rent_by_neighborhood[neighborhood]['total_price']/rent_by_neighborhood[neighborhood]['units']



        def calculate_rent_by_num_bedrooms():
            """ Gets rent average by unit size. """

            rent_by_num_bedrooms = {}
            units = 0


        # def calculate_rent_by_num_bedrooms():
            # rent_by_sqft_range = {}



        average_rent_by_neighborhood = calculate_rent_by_neighborhood()
        average_rent_by_num_bedrooms = calculate_rent_by_num_bedrooms()

