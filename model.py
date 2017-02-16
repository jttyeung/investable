from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from datetime import datetime


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

    def __repr__(self):
        """ Shows information on the unit details of the unit up for rent or for sale. """

        return '<UnitDetails id=%s description=%s price=%s>' % (self.home_id, self.description, self.price)


class Listing(db.Model):
    """ Unit sale listings. """

    __tablename__ = 'listings'

    home_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Integer, nullable=False)
    HOA = db.Column(db.Integer, nullable=True)
    photo_url = db.Column(db.String(2083), nullable=True)
    detail_id = db.Column(db.Integer, db.ForeignKey('unitdetails.detail_id'), nullable=False)

    unitdetails = db.relationship('UnitDetails', backref='listings')


    def __repr__(self):
        """ Shows information about the unit up for sale. """

        return '<Listing id=%s price=%s hoa=%s detail_id=%s>' % (self.home_id, self.price, self.hoa, self.detail_id)


class Rental(db.Model):
    """ Unit rental listings. """

    __tablename__ = 'rentals'

    cl_id = db.Column(db.String(150), primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    detail_id = db.Column(db.Integer, db.ForeignKey('unitdetails.detail_id'), nullable=False)

    unitdetails = db.relationship('UnitDetails', backref='rentals')


    def __repr__(self):
        """ Shows information about the unit up for rent. """

        return '<Rental id=%s description=%s price=%s detail_id=%s>' % (self.cl_id, self.price, self.date_saved, self.detail_id)


class Favorite(db.Model):
    """ Favorite homes. """

    __tablename__ = 'favorites'

    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey('listings.home_id'), nullable=False)
    date_saved = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    users = db.relationship('User', backref='favorites')
    listings = db.relationship('Listing', backref='favorites')

    def __repr__(self):
        """ Shows the user's favorite homes. """

        return '<Favorite id=%s user_id=%s home_id=%s date_saved=%s>' % (self.favorite_id, self.user_id, self.home_id, self.date_saved)



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
