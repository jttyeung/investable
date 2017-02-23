from server import *
from model import *


def get_avg_rent(bedrooms, bathrooms, sqft, latlng_point):
    """ Gets the average rent within search radius. """

    # Search radius distance in meters. 1609 meters ~ 1 mile
    SEARCH_RADIUS = 3219

    # Search average rent price by radius by accuracy of number of bedrooms
    avg_rent_by_br = int(db.session.query(func.avg(Rental.price)).join(UnitDetails).filter((func.ST_Distance_Sphere(latlng_point, UnitDetails.latlng) < SEARCH_RADIUS) & (UnitDetails.bedrooms == bedrooms)).all()[0][0])

    # # Future functionality:
    # # Search average rent price by radius by accuracy of number of bedrooms and bathrooms
    # avg_rent_by_br_ba = db.session.query(func.avg(Rentals.price)).join(UnitDetails).filter((func.ST_Distance_Sphere(latlng_point, UnitDetails.latlng) < SEARCH_RADIUS) & (UnitDetails.bedrooms == bedrooms) & (UnitDetails.bathrooms == bathrooms)).all()[0][0]

    # Search average rent price by radius by accuracy of sqft range per (+) or (-) 250 sqft
    avg_rent_by_sqft = int(db.session.query(func.avg(Rental.price)).join(UnitDetails).filter((func.ST_Distance_Sphere(latlng_point, UnitDetails.latlng) < SEARCH_RADIUS) & (UnitDetails.sqft.between(UnitDetails.sqft - 250, UnitDetails.sqft + 250))).all()[0][0])

    return { 'avg_rent_by_br': avg_rent_by_br, 'avg_rent_by_sqft': avg_rent_by_sqft }


    # # TEST QUERY:
    # db.session.query(func.avg(Rental.price)).join(UnitDetails).filter((func.ST_Distance_Sphere('POINT(37.7651614 -122.460148)', UnitDetails.latlng) < 1409) & (UnitDetails.bedrooms == 1) & (UnitDetails.bathrooms == 1) & (UnitDetails.sqft > 700)).all()[0][0]


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
                              price=price,
                              hoa=listing['hoa'],
                              unitdetails=new_unit_details)

        db.session.add(new_listing)

        db.session.commit()

    except:
        db.session.rollback()
