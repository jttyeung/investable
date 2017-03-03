""" Investable Server """

from flask import Flask, render_template, redirect, flash, request, jsonify, json
from flask_debugtoolbar import DebugToolbarExtension

import jinja2
import os
import geocoder

from zillow_utilities import *
from account_utilities import *
from mortgage_calculator import *
from db_queries import *
from model import *


app = Flask(__name__)

app.secret_key = os.environ['APP_KEY']
app.zwsid = os.environ['ZWSID']
app.gmaps = os.environ['GMAPS_JS']

# jinja debugger
app.jinja_env.undefined = jinja2.StrictUndefined
app.jinja_env.auto_reload = True


##############################################################################
# Route definitions

@app.route('/')
def homepage():
    """ Brings user to the homepage. """

    return render_template('index.html', GMAPS_JS=app.gmaps)


@app.route('/search.json')
def search():
    """ Returns user search results from Zillow's API and PostgreSQL. """

    # Search address entered by the user
    full_address = {}
    full_address.update(request.args.items())

    # Gets API response data from zillow_utilities
    response_code, price, message, hoa = get_unit_price(full_address)

    # If the location is found in Zillow's API
    if response_code == 100:
        unit_details = get_zillow_unit_details(full_address)

        # Returns the response code and unit details from Zillow's API and PostgreSQL
        listing = { 'response': response_code,
                    'price': price,
                    'message': message,
                    'neighborhood': unit_details['neighborhood'],
                    'street': unit_details['street'],
                    'city': unit_details['city'],
                    'state': unit_details['state'],
                    'zipcode': unit_details['zipcode'],
                    'bedrooms': unit_details['bedrooms'],
                    'bathrooms': unit_details['bathrooms'],
                    'sqft': unit_details['sqft'],
                    'hoa': hoa,
                    'latitude': unit_details['latitude'],
                    'longitude': unit_details['longitude'],
                    'latlng_point': unit_details['latlng_point'],
                    'zpid': unit_details['zpid']
                    }

        # Adds a listing to the database
        add_listing_to_db(listing)

    else:
        listing = { 'response': response_code, 'price': price, 'message': message }

    return jsonify(listing)


@app.route('/avgrent.json')
def get_rent_avgs():
    """ Gets average rent data from db_queries. """

    listing = request.args.get('listing')
    listing_dict = json.loads(listing)

    # If source data contains a latlng_point
    if listing_dict.get('latlng_point'):
        latlng_point = listing_dict['latlng_point']
    # Otherwise, make a latlng point
    else:
        latlng_point = 'POINT({} {})'.format(listing_dict['latitude'],listing_dict['longitude'])

    rent_avgs = get_avg_rent(listing_dict['bedrooms'], listing_dict['bathrooms'], listing_dict['sqft'], latlng_point)

    return jsonify(rent_avgs)


@app.route('/listings.json')
def get_listings():
    """ Finds listings in the area filtered by bedrooms, bathrooms, and/or prices. """

    bounds = json.loads(request.args.get('geoBounds'))
    bedrooms = float(request.args.get('bedroomFilter'))
    bathrooms = float(request.args.get('bathroomFilter'))
    low_price = int(request.args.get('lowPrice'))
    high_price = int(request.args.get('highPrice'))

    # Retrieves listings from db_queries
    filtered_listings = find_all_listings(bounds, bedrooms, bathrooms, low_price, high_price)

    return jsonify(filtered_listings)


@app.route('/calculator')
def calculate_monthly_payment():
    """ Calculates the monthly mortgage payment based on user's details. """

    # User data pulled from AJAX
    mortgage_details = {}
    mortgage_details.update(request.args.items())
    mortgage, hoa_mortgage, total_mortgage = calculate_mortgage(mortgage_details)

    return jsonify({ 'mortgage': mortgage, 'hoa_mortgage': hoa_mortgage, 'total_mortgage': total_mortgage })


@app.route('/login', methods=['GET'])
def login():
    """ Brings user to the login page. """

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def verify_login():
    """ Verifys user's login. """
    email = request.form.get('email')
    password = request.form.get('password')

    return redirect('/')


@app.route('/register', methods=['GET'])
def register():
    """ Brings user to the registration page. """

    return render_template('registration.html')


@app.route('/register', methods=['POST'])
def registration_complete():
#     """ Processes a new user registration. """

    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')

    add_registration(firstname, lastname, email, password)

#     if username exists:
#         flash('Sorry, that email has already been registered. Login instead?')
#         return redirect('/register')

#     else create a new user:
#         flash('You have successfully created an account. Please login to continue.')
#         return redirect('/')

    return redirect('/')


@app.route('/account')
def account_details():
    """ Shows a user's account details. """

    return render_template('account.html')


##############################################################################
# Helper functions

if __name__ == "__main__":
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    # Connect DB to Flask before running app
    connect_to_db_flask(app)

    app.run(host="0.0.0.0", port=5000)
