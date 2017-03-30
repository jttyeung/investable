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

    # Query for the listings in the database within the latitude and
    # longitude bounds of the user's search with respect to any filters
    listings = db.session.query(Listing).join(UnitDetails).filter((bounds['west'] < UnitDetails.longitude), (bounds['east'] > UnitDetails.longitude), (bounds['north'] > UnitDetails.latitude), (bounds['south'] < UnitDetails.latitude), (UnitDetails.bedrooms >= bedrooms), (UnitDetails.bathrooms >= bathrooms), (Listing.price >= low_price), (Listing.price <= high_price)).all()

    all_listings = []

    for listing in listings:
        all_listings.append({'response': 100,  # found listing response
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

    return all_listings
