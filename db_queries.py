from server import *
from model import *



def get_avg_rent(latlng_point):
    """ Gets the average rent within search radius """

    # Search radius distance in meters. 1609 meters ~ 1 mile
    SEARCH_RADIUS = 3219

    print latlng_point + '$&*%^(^&@'*20

    # Search average rent price by radius by accuracy of number of bedrooms
    avg_rent_by_br = db.session.query(func.avg(Rental.price)).join(UnitDetails).filter((func.ST_Distance_Sphere(latlng_point, UnitDetails.latlng) < SEARCH_RADIUS) & (UnitDetails.bedrooms == bedrooms)).all()[0][0]

    # Search average rent price by radius by accuracy of number of bedrooms and bathrooms
    # avg_rent_by_br_ba = db.session.query(func.avg(Rentals.price)).join(UnitDetails).filter((func.ST_Distance_Sphere(latlng_point, UnitDetails.latlng) < SEARCH_RADIUS) & (UnitDetails.bedrooms == bedrooms) & (UnitDetails.bathrooms == bathrooms)).all()[0][0]

    # Search average rent price by radius by accuracy of sqft range per (+) or (-) 250 sqft
    avg_rent_by_sqft = db.session.query(func.avg(Rental.price)).join(UnitDetails).filter((func.ST_Distance_Sphere(latlng_point, UnitDetails.latlng) < SEARCH_RADIUS) & (UnitDetails.sqft.between(UnitDetails.sqft - 250, UnitDetails.sqft + 250))).all()[0][0]

    return { 'avg_rent_by_br': avg_rent_by_br, 'avg_rent_by_sqft': avg_rent_by_sqft }


    # TEST QUERY:
    # db.session.query(func.avg(Rental.price)).join(UnitDetails).filter((func.ST_Distance_Sphere('POINT(37.7651614 -122.460148)', UnitDetails.latlng) < 1409) & (UnitDetails.bedrooms == 1) & (UnitDetails.bathrooms == 1) & (UnitDetails.sqft > 700)).all()[0][0]
