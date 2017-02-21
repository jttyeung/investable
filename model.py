from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, between
from sqlalchemy.engine.url import URL

from datetime import datetime
from geoalchemy2 import Geometry


db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """ User information. """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        """ Shows information about the user. """

        return '<User id=%s firstname=%s lastname=%s email=%s>' % (self.user_id, self.firstname, self.lastname, self.email)


class UnitDetails(db.Model):
    """ Details of the unit for sale or up for rent. """

    __tablename__ = 'unitdetails'

    detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    neighborhood = db.Column(db.String(150), nullable=False)
    bedrooms = db.Column(db.Float, nullable=True)
    bathrooms = db.Column(db.Float, nullable=True)
    sqft = db.Column(db.Integer, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latlng = db.Column(Geometry(geometry_type='POINT'), nullable=False)


    def __repr__(self):
        """ Shows unit details of the unit for rent or sale. """

        return '<UnitDetails id=%s neighborhood=%s latitude=%s longitude=%s latlng=%s>' % (self.detail_id, self.neighborhood, self.latitude, self.longitude, self.latlng)


class Listing(db.Model):
    """ Unit sale listings. """

    __tablename__ = 'listings'

    listing_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Integer, nullable=False)
    photo_url = db.Column(db.String(2083), nullable=True)
    detail_id = db.Column(db.Integer, db.ForeignKey('unitdetails.detail_id'), nullable=False)

    unitdetails = db.relationship('UnitDetails', backref='listings')


    def __repr__(self):
        """ Shows information about the unit for sale. """

        return '<Listing id=%s price=%s detail_id=%s>' % (self.listing_id, self.price, self.detail_id)


class Rental(db.Model):
    """ Unit rental listings. """

    __tablename__ = 'rentals'

    cl_id = db.Column(db.String(150), primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    detail_id = db.Column(db.Integer, db.ForeignKey('unitdetails.detail_id'), nullable=False)

    unitdetails = db.relationship('UnitDetails', backref='rentals')


    def __repr__(self):
        """ Shows information about the unit for rent. """

        return '<Rental id=%s price=%s data_posted=%s detail_id=%s>' % (self.cl_id, self.price, self.date_posted, self.detail_id)


class Favorite(db.Model):
    """ Favorite homes. """

    __tablename__ = 'favorites'

    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.listing_id'), nullable=False)
    date_saved = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    users = db.relationship('User', backref='favorites')
    listings = db.relationship('Listing', backref='favorites')


    def __repr__(self):
        """ Shows the user's favorite homes. """

        return '<Favorite id=%s user_id=%s listing_id=%s date_saved=%s>' % (self.favorite_id, self.user_id, self.listing_id, self.date_saved)


##############################################################################
# Sample data

def sample_data():
    """ Create sample data for test database. """

    # In case this is run more than once, empty out existing data
    User.query.delete()
    UnitDetails.query.delete()
    Listing.query.delete()
    Rental.query.delete()
    Favorite.query.delete()

    # Add sample users
    fiyero = User(firstname=fiyero, lastname=tigelaar, email='fiyerotigelaar@example.com', password='')
    wizard = User(firstname=wizard, lastname=ofoz, email='wizardofoz@example.com', password='')
    elphaba = User(firstname=elphaba, lastname=thropp, email='elphabathropp@example.com', password='')
    glinda = User(firstname=glinda, lastname=good, email='glindagood@example.com', password='')

    # Add sample unit details
    detail1 = UnitDetails(neighborhood='inner sunset / UCSF', bedrooms=2, bathrooms=2.5, sqft=2500, latitude=37.7651614, longitude=-122.4601482, latlng='0101000000AE940ACFF0E142400D946F11739D5EC0')
    detail2 = UnitDetails(neighborhood='tenderloin', bedrooms=0, bathrooms=1, sqft=390, latitude=37.78526, longitude=-122.411953, latlng='0101000000B16D516683E442404D9F1D705D9A5EC0')
    detail3 = UnitDetails(neighborhood='pacific heights', bedrooms=1, bathrooms=1, sqft=650, latitude=37.7958617, longitude=-122.3945241, latlng='0101000000C4C02962C7E44240F7BE02E23F995EC0')
    detail4 = UnitDetails(neighborhood='noe valley', bedrooms=4, bathrooms=3, sqft=1740, latitude=37.7503705, longitude=-122.436254, latlng='01010000000CB1FA230CE04240F3AFE595EB9B5EC0')
    detail5 = UnitDetails(neighborhood='lower nob hill', bedrooms=2, bathrooms=1.5, sqft=1190, latitude=37.7872375, longitude=-122.4139991, latlng='0101000000A857CA32C4E44240B3C414F67E9A5EC0')
    detail6 = UnitDetails(neighborhood='russian hill', bedrooms=2, bathrooms=1, sqft=1400, latitude=37.7960949, longitude=-122.4133919, latlng='010100000096010C70E6E542409ABB4C03759A5EC0')
    detail7 = UnitDetails(neighborhood='pacific heights', bedrooms=1, bathrooms=1, sqft=760, latitude=37.789962, longitude=-122.4256378, latlng='0101000000988A8D791DE5424040BC53A63D9B5EC0')
    detail8 = UnitDetails(neighborhood='inner sunset / UCSF', bedrooms=4, bathrooms=1.5, sqft=1940, latitude=37.7639145, longitude=-122.4695433, latlng='0101000000583849F3C7E14240946357FF0C9E5EC0')
    detail9 = UnitDetails(neighborhood='lower nob hill', bedrooms=5, bathrooms=3, sqft=2180, latitude=37.7912167, longitude=-122.4157727, latlng='01010000004746BD9646E54240754419059C9A5EC0')
    detail10 = UnitDetails(neighborhood='downtown / civic / van ness', bedrooms=2, bathrooms=2, sqft=2500, latitude=37.7815058, longitude=-122.4204841, latlng='01010000003151CE6108E442403B7F2436E99A5EC0')

    # Add sample listings
    listing1 = Listing(price=1105500, detail_id=detail1)
    listing2 = Listing(price=550900, detail_id=detail2)
    listing3 = Listing(price=664000, detail_id=detail3)
    listing4 = Listing(price=2540800, detail_id=detail4)
    listing5 = Listing(price=980430, detail_id=detail5)

    # Add sample rentals
    rental1 = Rental(cl_id=6007117641, price=2890, date_posted='2017-02-17 07:27:17+00', detail_id=detail6)
    rental2 = Rental(cl_id=6007117642, price=1885, date_posted='2017-02-17 07:03:38+00', detail_id=detail7)
    rental3 = Rental(cl_id=6007117643, price=5460, date_posted='2017-02-14 22:30:45+00', detail_id=detail8)
    rental4 = Rental(cl_id=6007117644, price=6700, date_posted='2017-02-15 04:58:04+00', detail_id=detail9)
    rental5 = Rental(cl_id=6007117645, price=3155, date_posted='2017-02-18 00:19:55+00', detail_id=detail10)

    # Add sample favorites
    favorite1 = Favorite(user_id=fiyero, listing_id=listing3, date_saved='2017-01-18 21:11:35.537000')
    favorite2 = Favorite(user_id=elphaba, listing_id=listing3, date_saved='2017-02-01 17:51:43.235000')
    favorite3 = Favorite(user_id=elphaba, listing_id=listing1, date_saved='2017-02-10 11:08:51.067000')
    favorite4 = Favorite(user_id=elphaba, listing_id=listing5, date_saved='2017-02-13 12:36:12.473000')
    favorite5 = Favorite(user_id=glinda, listing_id=listing3, date_saved='2017-02-16 14:27:36.182000')

    # Add and commit to test database
    db.session.add_all([fiyero, wizard, elphaba, glinda,
                        detail1, detail2, detail3, detail4, detail5,
                        detail6, detail7, detail8, detail9, detail10,
                        listing1, listing2, listing3, listing4, listing5,
                        rental1, rental2, rental3, rental4, rental5,
                        favorite1, favorite2, favorite3, favorite4, favorite5
                        ])
    db.session.commit()


##############################################################################
# Helper functions

def connect_to_db_scrapy():
    """ Connects the database to Scrapy via a session. """

    engine = create_engine('postgres:///investable', echo=False, encoding='utf8')
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def connect_to_db_flask(app):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///investable'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    # Import app from server if opening from this file
    from server import app

    connect_to_db_flask(app)
    print "Connected to DB."

    # In case tables haven't been created, create them
    db.create_all()
