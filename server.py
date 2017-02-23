""" Investable Server """

from flask import Flask, render_template, redirect, flash, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import jinja2
import os

from zillow_utilities import *
from account_utilities import *
from mortgage_calculator import *
from db_queries import *
from model import *


app = Flask(__name__)

app.secret_key = os.environ['APP_KEY']
app.zwsid = os.environ['ZWSID']

# jinja debugger
app.jinja_env.undefined = jinja2.StrictUndefined
app.jinja_env.auto_reload = True


##############################################################################
# Route definitions

@app.route('/')
def homepage():
    """ Brings user to the homepage. """

    return render_template('index.html')


@app.route('/search.json')
def search():
    """ Returns user search results from Zillow's API and PostgreSQL. """

    # Search address entered by the user
    full_address = {}
    full_address.update(request.args.items())

    # Gets API response data from zillow_utilities
    response_code, price, hoa = get_unit_price(full_address)

    # If the location is found in Zillow's API
    if response_code == 100:
        unit_details = get_zillow_unit_details(full_address)
        # neighborhood = get_neighborhood(full_address)
        # bedrooms = get_bedrooms(full_address)
        # bathrooms = get_bathrooms(full_address)
        # sqft = get_sqft(full_address)
        # latlng_point = get_latlong(full_address)

        # Gets rent average data from db_queries
        rent_avgs = get_avg_rent(unit_details['bedrooms'], unit_details['bathrooms'], unit_details['sqft'], unit_details['latlng_point'])
        # rent_avgs = get_avg_rent(bedrooms, bathrooms, sqft, latlng_point)

        # Returns the response code and unit details from Zillow's API and PostgreSQL
        listing = { 'response': response_code, 'price': price, 'neighborhood': unit_details['neighborhood'], 'bedrooms': unit_details['bedrooms'], 'bathrooms': unit_details['bathrooms'], 'sqft': unit_details['sqft'], 'hoa': hoa, 'latitude': unit_details['latitude'], 'longitude': unit_details['longitude'], 'latlng_point': unit_details['latlng_point'], 'rent_avgs': rent_avgs, 'zpid': unit_details['zpid'] }
        # listing = { 'response': response_code, 'price': price, 'neighborhood': neighborhood, 'bedrooms': bedrooms, 'bathrooms': bathrooms, 'sqft': sqft, 'rent_avgs': rent_avgs }

        # Adds a listing to the database
        add_listing_to_db(listing)

    else:
        listing = { 'response': response_code, 'price': price }

    return jsonify(listing)


@app.route('/calculator')
def calculate_monthly_payment():
    """ Calculates the monthly mortgage payment based on user's details. """

    # User data pulled from AJAX
    mortgage_details = {}
    mortgage_details.update(request.args.items())
    mortgage, total_mortgage = calculate_mortgage(mortgage_details)

    return jsonify({ 'mortgage': mortgage, 'total_mortgage': total_mortgage })


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
