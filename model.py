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


class Home(db.Model):
    """ Home listings. """

    __tablename__ = 'homes'

    home_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    HOA = db.Column(db.Integer, nullable=True)
    photo_url = db.Column(db.String(2083), nullable=True)
    neighborhood_id = db.Column(db.Integer, db.ForeignKey(neighborhoods.neighborhood_id))
    size_id = db.Column(db.Integer, db.ForeignKey(sizes.size_id))


    def __repr__(self):
        """ Shows information about the home. """

        return '<Home id=%s description=%s price=%s>' % (self.home_id, self.description, self.price)


class Neighborhood(db.Model):
    """ Neighborhoods defined on Craigslist. """

    __tablename__ = 'neighborhoods'

    neighborhood_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)


    def __repr__(self):
        """ Shows neighborhood information. """

        return '<Neighborhood id=%s name=%s>' % (self.neighborhood_id, self.name)


class Rent(db.Model):
    """ Rental listings. """

    __tablename__ = 'rents'

    rental_id = db.Column(db.Integer, primary_key=True, autoincrement=True)


    def __repr__(self):
        """ Shows average rent information. """

        rent_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        neighborhood_id = db.Column(db.Integer, db.ForeignKey(neighborhoods.neighborhood_id), nullable=False)
        size_id = db.Column(db.Integer, db.ForeignKey(sizes.size_id), nullable=False)
        avg_rent = db.Column(db.Integer, nullable=False)

        return '<Rental id=%s avg_rent=%s size=%s neighborhood=%s>' % (self.rent_id, self.avg_rent, self.size_id, self.neighborhood_id)


class Favorite(db.Model):
    """ Favorite homes. """

    __tablename__ = 'favorites'

    favorite_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(users.user_id), nullable=False)
    home_id = db.Column(db.Integer, db.ForeignKey(homes.home_id), nullable=False)
    date_saved = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def __repr__(self):
        """ Shows the user's favorite homes. """

        return '<Favorite id=%s user_id=%s home_id=%s date_saved=%s>' % (self.favorite_id, self.user_id, self.home_id, self.date_saved)


class Size(db.Model):
    """ Home and rental sizes. """

    __tablename__ = 'sizes'

    size_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bedrooms = db.Column(db.Integer, nullable=True)
    bathrooms = db.Column(db.Integer, nullable=True)
    sqft = db.Column(db.Integer, nullable=True)


    def __repr__(self):
        """ Shows the home and rental sizes. """

        return '<Size id=%s bedrooms=%s bathrooms=%s sqft=%s>' % (self.size_id, self.bedrooms, self.bathrooms, self.sqft)



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
