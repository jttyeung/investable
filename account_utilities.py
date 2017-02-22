import bcrypt

from model import *
from server import *


def hash_password(password):
    """ Hash a password for the first time, with a randomly-generated salt. """

    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    return hashed


def add_registration(firstname, lastname, email, password):
    """ Takes user details and hashed password and adds a new user record to the database. """

    hashed = hash_password(password)

    new_user = User(firstname=firstname, lastname=lastname, email=email, password=hashed)
    db.session.add(new_user)
    db.session.commit()


def check_password(email, password, hashed):
    """ Check that an unhashed password matches one that has previously been hashed. """

    user = User.query.filter(email=email).first()
    hashed = user.password

    if bcrypt.checkpw(password, hashed):
        print "It Matches!"
    else:
        print "It Does not Match :("
