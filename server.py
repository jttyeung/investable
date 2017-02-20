""" Investable Server """

from flask import Flask, render_template, redirect, flash, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import jinja2
import os

from zillow_utilities import *
from mortgage_calculator import *
from db_queries import *


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
    """ Returns user search results. """

    # User search data from site
    full_address = {}
    full_address.update(request.args.items())

    # Gets response data from zillow_utilities
    response_code, price = get_unit_price(full_address)
    neighborhood = get_neighborhood(full_address)
    latlng_point = get_latlong(full_address)
    print latlng_point
    print '-'*100

    # Gets rent average data from db_queries
    rent_avgs = get_avg_rent(latlng_point)
    print rent_avgs
    print '*'*100

    # Returns the response code, list price, neighborhood, and rent average
    listing = { 'response': response_code, 'price': price, 'neighborhood': neighborhood, 'avg_rent_by_br': avg_rent_by_br, 'avg_rent_by_sqft': avg_rent_by_sqft }
    print listing
    print '#'*100

    return jsonify(listing)

    # need to determine where search lands user - same page, refreshed page, etc.


# @app.route('/rent.json')
# def calculate_monthly_rent():
#     """ Returns user search results. """

#     # User search data from site
#     full_address = {}
#     full_address.update(request.args.items())

#     # Get unit lat/lng point
#     latlng_point = get_latlong(full_address)

#     # Gets rent average data from db_queries
#     rent_avgs = get_rent_avg(latlng_point)

#     # Returns the rent averages
#     rent_avgs = { 'avg_rent_by_br': avg_rent_by_br, 'avg_rent_by_sqft': avg_rent_by_sqft }

#     return jsonify(rent_avgs)


@app.route('/calculator')
def calculate_monthly_payment():
    """ Calculates the monthly mortgage payment based on user's details. """

    # User data pulled from AJAX
    mortgage_details = {}
    mortgage_details.update(request.args.items())
    mortgage, total_mortgage = calculate_mortgage(mortgage_details)

    return jsonify({ 'mortgage': mortgage, 'total_mortgage': total_mortgage })


@app.route('/login')
def login():
    """ Brings user to the login page. """

    return render_template('login.html')


@app.route('/register', methods=['GET'])
def register():
    """ Brings user to the registration page. """

    return render_template('registration.html')


# @app.route('/register', methods=['POST'])
# def add_user_registration():
#     """ Processes a new user registration. """

#     if username exists:
#         flash('Sorry, that email has already been registered. Login instead?')
#         return redirect('/register')

#     else create a new user:
#         flash('You have successfully created an account. Please login to continue.')
#         return redirect('/')


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

    app.run(host="0.0.0.0", port=5000)
