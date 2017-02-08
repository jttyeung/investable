""" Investable Server """

from flask import Flask, render_template, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension

import jinja2
import os
import urllib
from bs4 import BeautifulSoup


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


@app.route('/search')
def search():
    """ Returns user search results. """

    # Uses user search to query Zillow's API and returns API response
    address = request.args.get('street')
    citystatezip = request.args.get('citystatezip')
    formatted_full_address = address.replace(' ','-') + '-' + citystatezip.replace(' ','-')
    print '-------------'+ formatted_full_address + '-------------------'
    search_location = {'address': address, 'citystatezip': citystatezip}
    result = 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=' + app.zwsid + '&' + urllib.urlencode(search_location)

    # Scrapes unit_id from API response using BeautifulSoup
    html = urllib.urlopen(result).read()
    soup = BeautifulSoup(html, "html.parser")
    unit_id = soup.find('zpid').getText()

    print '-------------'+ unit_id + '-------------------'

    # Using unit_id, finds unit's page on Zillow and scrapes unit's listing price
    zillow_page = 'http://www.zillow.com/homedetails/{}/{}_zpid/'.format(formatted_full_address, unit_id)
    zillow_html = urllib.urlopen(zillow_page).read()
    zillow_soup = BeautifulSoup(zillow_html, "html.parser")

    def get_unit_price():
        """Gets listing price of unit on Zillow"""

        unit_price_string = str(zillow_soup.find('div', class_='main-row home-summary-row').find('span'))
        unit_price = unit_price_string[unit_price_string.index('$') : unit_price_string.index(' <span class="value-suffix">')]

        return unit_price

    return get_unit_price()
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
