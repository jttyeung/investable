""" Investable Server """

from flask import Flask, render_template, redirect, flash, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import jinja2
import os

from zillow_utilities import *



app = Flask(__name__)

app.secret_key = os.environ['APP_KEY']
app.zwsid = os.environ['ZWSID']

# jinja debugger
app.jinja_env.undefined = jinja2.StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/')
def homepage():
    """ Brings user to the homepage. """

    return render_template('index.html')


@app.route('/search.json')
def search():
    """ Returns user search results. """

    # Takes user search to query Zillow's API and returns API response
    full_address = {}
    full_address.update(request.args.items())
    listing = { 'price': get_unit_price(full_address) }

    try:
        int(listing['price'])
        return jsonify(listing)

    except ValueError:
        flash('Sorry, we are unable to find a matching home with that address. Please try searching again.')
        return ""

    # return get_unit_price(full_address)
    # need to determine where search lands user - same page, refreshed page, etc.
    # return result

    # try to figure out how to get XML <message><code> from resulting api call. '0' means 'Request successfully processed', but what if call returns no results?
    # code 508 is 'Error: no exact match found for input address'


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


if __name__ == "__main__":
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0", port=5000)
