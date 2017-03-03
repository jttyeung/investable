from server import *
from model import *


def get_avg_rent(bedrooms, bathrooms, sqft, latlng_point):
    """ Gets the average rent within search radius. """

    # Search radius distance in meters. 1609 meters ~ 1 mile
    SEARCH_RADIUS = 3219

    # Search within + and - this amount of sqft difference
    SEARCH_SQFT_RANGE = 250

    try:
        # Search average rent price by radius by accuracy of number of bedrooms
        avg_rent_by_br = int(db.session.query(func.avg(Rental.price)).join(UnitDetails).filter((func.ST_Distance_Sphere(latlng_point, UnitDetails.latlng) < SEARCH_RADIUS) & (UnitDetails.bedrooms == bedrooms)).all()[0][0])
    except TypeError:
        avg_rent_by_br = 'Not enough rental data nearby to calculate an average.'

    try:
        # Search average rent price by radius by accuracy of sqft range per (+) or (-) 250 sqft
        avg_rent_by_sqft = int(db.session.query(func.avg(Rental.price)).join(UnitDetails).filter((func.ST_Distance_Sphere(latlng_point, UnitDetails.latlng) < SEARCH_RADIUS) & (UnitDetails.sqft.between(UnitDetails.sqft - SEARCH_SQFT_RANGE, UnitDetails.sqft + SEARCH_SQFT_RANGE))).all()[0][0])
    except TypeError:
        avg_rent_by_sqft = 'Not enough rental data nearby to calculate an average.'

    return { 'avg_rent_by_br': avg_rent_by_br, 'avg_rent_by_sqft': avg_rent_by_sqft }


def add_listing_to_db(listing):
    """ Adds a unit listing to the database. """

    latlng = 'POINT({} {})'.format(listing['latitude'], listing['longitude'])
    price = re.sub('[^\d.]+', '', listing['price'])

    try:
        new_unit_details = UnitDetails(neighborhood=listing['neighborhood'],
                                       bedrooms=listing['bedrooms'],
                                       bathrooms=listing['bathrooms'],
                                       sqft=listing['sqft'],
                                       latitude=listing['latitude'],
                                       longitude=listing['longitude'],
                                       latlng=latlng
                                       )

        db.session.add(new_unit_details)

        new_listing = Listing(zpid=listing['zpid'],
                              street=listing['street'],
                              city=listing['city'],
                              state=listing['state'],
                              zipcode=listing['zipcode'],
                              price=price,
                              hoa=listing['hoa'],
                              unitdetails=new_unit_details)

        db.session.add(new_listing)

        db.session.commit()

    except:
        db.session.rollback()


def find_all_listings(bounds, bedrooms, bathrooms, low_price, high_price):
    """ Finds all the listings within the geocoded location range. """

    # Number of listing results that can be returned at once
    MAX_QUERY_RESULTS = 50

    # Query for the listings in the database within the latitude and
    # longitude bounds of the user's search with respect to any filters
    listings = db.session.query(Listing).join(UnitDetails).filter((bounds['west'] < UnitDetails.longitude), (bounds['east'] > UnitDetails.longitude), (bounds['north'] > UnitDetails.latitude), (bounds['south'] < UnitDetails.latitude), (UnitDetails.bedrooms >= bedrooms), (UnitDetails.bathrooms >= bathrooms), (Listing.price >= low_price), (Listing.price <= high_price)).all()

    # Query with limitations on max results
    # listings = db.session.query(Listing).join(UnitDetails).filter((bounds['west'] < UnitDetails.longitude), (bounds['east'] > UnitDetails.longitude), (bounds['north'] > UnitDetails.latitude), (bounds['south'] < UnitDetails.latitude)).order_by(func.random()).limit(MAX_QUERY_RESULTS).all()

    listings_latlng = []

    for listing in listings:
        listings_latlng.append({'response': 100,  # mock api found listing response
                                'latitude': listing.unitdetails.latitude,
                                'longitude': listing.unitdetails.longitude,
                                'street': listing.street,
                                'city': listing.city,
                                'state': listing.state,
                                'zipcode': listing.zipcode,
                                'price': listing.price,
                                'hoa': listing.hoa,
                                'bedrooms': listing.unitdetails.bedrooms,
                                'bathrooms': listing.unitdetails.bathrooms,
                                'sqft': listing.unitdetails.sqft,
                                'zpid': listing.zpid
                                })

    return listings_latlng



    # sample
    # bounds = {'west': -123.17382499999997, 'east': -122.28178000000003, 'north': 37.9298239, 'south': 37.6398299}

    #     ST_GeomFromText('POLYGON(   (-71.1776585052917 42.3902909739571,-71.1776820268866 42.3903701743239,-71.1776063012595 42.3903825660754,-71.1775826583081 42.3903033653531,-71.1776585052917 42.3902909739571)    )');


    # if bounds.west <= db.session.query(UnitDetails.longitude) and db.session.query(UnitDetails.latitude) <= bounds.east and bounds.north <= p.y and p.y <= bounds.south:
    #     print db.session.query(UnitDetails.latitude, UnitDetails.longitude)


    # listings = db.session.query(Listing.zpid).join(UnitDetails).filter(func.ST_Contains(ST_GeomFromText('POLYGON((-123.17382499999997 37.9298239,-122.28178000000003 37.6398299))'),UnitDetails.latlng) == TRUE)

    # listings = db.session.query(Listing.zpid).join(UnitDetails).filter(func.ST_Contains(ST_GeomFromText('POLYGON((-123.17382499999997 37.9298239,-122.28178000000003 37.6398299))'),UnitDetails.latlng) == TRUE)










