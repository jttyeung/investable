from flask_sqlalchemy import SQLAlchemy
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
    bedrooms = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Integer, nullable=True)
    sqft = db.Column(db.Integer, nullable=True)
    latitude = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """ Shows information on the unit details of the unit up for rent or for sale. """

        return '<Home id=%s description=%s price=%s>' % (self.home_id, self.description, self.price)


class ForSale(db.Model):
    """ Unit sale listings. """

    __tablename__ = 'selling'

    home_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Integer, nullable=False)
    HOA = db.Column(db.Integer, nullable=True)
    photo_url = db.Column(db.String(2083), nullable=True)
    detail_id = db.Column(db.Integer, db.ForeignKey('unitdetails.detail_id'), nullable=False)

    unitdetails = db.relationship('UnitDetails', backref='selling')


    def __repr__(self):
        """ Shows information about the unit up for sale. """

        return '<ForSale id=%s price=%s hoa=%s detail_id=%s>' % (self.home_id, self.price, self.hoa, self.detail_id)


class ForRent(db.Model):
    """ Unit rental listings. """

    __tablename__ = 'renting'

    cl_id = db.Column(db.String(150), primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    detail_id = db.Column(db.Integer, db.ForeignKey('unitdetails.detail_id'), nullable=False)

    unitdetails = db.relationship('UnitDetails', backref='renting')


    def __repr__(self):
        """ Shows information about the unit up for rent. """

        return '<ForRent id=%s description=%s price=%s detail_id=%s>' % (self.cl_id, self.price, self.date_saved, self.detail_id)


class Favorite(db.Model):
    """ Favorite homes. """

    __tablename__ = 'favorites'

    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey('selling.home_id'), nullable=False)
    date_saved = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    users = db.relationship('User', backref='favorites')
    selling = db.relationship('ForSale', backref='favorites')

    def __repr__(self):
        """ Shows the user's favorite homes. """

        return '<Favorite id=%s user_id=%s home_id=%s date_saved=%s>' % (self.favorite_id, self.user_id, self.home_id, self.date_saved)



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///investable'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app


    connect_to_db(app)
    print "Connected to DB."
