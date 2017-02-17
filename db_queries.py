from server import *
from model import *


def get_avg_rent(latlng_point):
    """ Gets the average rent within search radius """

    # Search radius distance in meters. 1609 meters ~ 1 mile
    SEARCH_RADIUS = 3219


    # How do you make this query dynamic based on user input? Does it need to be dynamic?
    # User inputs: search returns a price of home and the latlng

    # MVP: Should return rent average of homes nearby within the radius of the comprable size
        # Stat 1: by bedrooms
        # Stat 2: by bed + bathrooms
        # Stat 3: by sqft -- range (0-500, 501-1000, 1001-1500, 1501-2000, 2001-2500, 2501-3000, 3001-3500, 3501-4000, etc)


    # See what average rental and home prices are in the city
    # See what average rental and home prices are by size in that city
    # See what average rental price is over time
    # See what average home price is over time
    # See what average price for homes in area is over time

    db.session.query(Rentals.price).filter(func.ST_Distance_Sphere(latlng_point, UnitDetails.latlng) < SEARCH_RADIUS).all()

    db.session.query(func.avg(Rental.price)).distinct().filter(func.ST_Distance_Sphere('POINT(37.7928478 -122.4267274)', UnitDetails.latlng) < 609).all()
