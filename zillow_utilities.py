import urllib
from bs4 import BeautifulSoup
from server import *


##############################################################################
# Formatting, Getting, and Parsing Results from Zillow

def format_api_url(full_address):
    """ Takes the address entered by user and returns a Zillow API encoded URL. """

    return 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=' + app.zwsid + '&' + urllib.urlencode(full_address)


def return_api_xml_parsed(full_address):
    """ Returns parsed XML data from Zillow's API. """

    api_url = format_api_url(full_address)
    api_xml = urllib.urlopen(api_url).read()
    api_xml_parsed = BeautifulSoup(api_xml, 'lxml-xml')
    api_response_code = int(api_xml_parsed.find('code').getText())

    return { 'api_response_code': api_response_code,
             'api_parsed_data': api_xml_parsed }




# def return_api_xml(full_address):
#     """ Returns parsed XML data from Zillow's API. """

#     api_url = format_api_url(full_address)
#     api_xml = urllib.urlopen(api_url).read()
#     return api_xml

# def parse_xml(xml):
#     api_xml_parsed = BeautifulSoup(api_xml, 'lxml-xml')
#     api_response_code = int(api_xml_parsed.find('code').getText())

#     return { 'api_response_code': api_response_code,
#              'api_parsed_data': api_xml_parsed }


# def funct(full_address):
#     xml = return_api_xml_parsed(full_address)
#     parse_xml(xml)



def get_zillow_html_page(full_address):
    """ Takes the API response and returns the HTML web address of the unit. """

    api_xml_parsed = return_api_xml_parsed(full_address)
    api_xml_data = api_xml_parsed['api_parsed_data']
    zillow_url = api_xml_data.find('homedetails').getText()

    return zillow_url


def return_html_parsed(full_address):
    """ Finds unit listing HTML page on Zillow and loads and parses the HTML response. """

    zillow_page = get_zillow_html_page(full_address)
    zillow_url = urllib.urlopen(zillow_page).geturl()
    zillow_html = urllib.urlopen(zillow_url).read()

    return BeautifulSoup(zillow_html, 'lxml')


##############################################################################
# Extracting Data From Zillow's API

def get_unit_price(full_address):
    """
    Extracts listing price of unit from Zillow's HTML listing page.

    Returns tuple of code and price and/or message. Codes are defined:
        100: Successful unit price received from Zillow page
        200: Found unit on Zillow's API, but unit is not listed for sale
        300: Could not match address location to API results
    """

    zillow_html_parsed = return_html_parsed(full_address)

    try:
        # Check if there is a listing price on Zillow
        unit_price_string = str(zillow_html_parsed.find('div', class_='main-row home-summary-row').find('span'))
        unit_price = unit_price_string[unit_price_string.index('$') : unit_price_string.index(' <span class="value-suffix">')]

        return (100, unit_price)

    except AttributeError:
        if get_zillow_price_estimate(full_address):
            # If unit is found off-market, look for a price estimate
            zillow_price_estimate = int(get_zillow_price_estimate(full_address))

            return (200, 'We found the unit you were searching for, but it\'s not currently for sale. Zillow\'s estimated current market value of that unit is ${:,}'.format(zillow_price_estimate))
        else:
            # Otherwise unit is not found/address entered is incorrect
            return (300, 'Sorry, we couldn\'t find a unit with that listing address. Please try your search again.')


def get_zillow_price_estimate(full_address):
    """ Scrapes the Zillow price estimate from API response if unit is not on the market. """

    api_xml_parsed = return_api_xml_parsed(full_address)
    api_response_code = api_xml_parsed['api_response_code']
    api_xml_data = api_xml_parsed['api_parsed_data']

    # Checks for a valid xml response code
    if api_response_code == 0:
        zillow_price_estimate = api_xml_data.find('amount').getText()

        return zillow_price_estimate


def get_neighborhood(full_address):
    """ Scrapes neighborhood name from Zillow's API response. """

    api_xml_parsed = return_api_xml_parsed(full_address)
    api_xml_data = api_xml_parsed['api_parsed_data']
    neighborhood = api_xml_data.find('region').get('name')

    return neighborhood


def get_latlong(full_address):
    """ Scrapes geolocation: latitude and longitude from Zillow's API response. """

    api_xml_parsed = return_api_xml_parsed(full_address)
    api_xml_data = api_xml_parsed['api_parsed_data']
    latitude = api_xml_data.find('latitude').getText()
    longitude = api_xml_data.find('longitude').getText()

    return 'POINT({} {})'.format(latitude, longitude)


def get_bedrooms(full_address):
    """ Scrapes number of bedrooms from Zillow's API response. """

    api_xml_parsed = return_api_xml_parsed(full_address)
    api_xml_data = api_xml_parsed['api_parsed_data']
    bedrooms = api_xml_data.find('bedrooms').getText()

    return float(bedrooms)


def get_bathrooms(full_address):
    """ Scrapes number of bathrooms from Zillow's API response. """

    api_xml_parsed = return_api_xml_parsed(full_address)
    api_xml_data = api_xml_parsed['api_parsed_data']
    bathrooms = api_xml_data.find('bathrooms').getText()

    return float(bathrooms)


def get_sqft(full_address):
    """ Scrapes unit sqft size from Zillow's API response. """

    api_xml_parsed = return_api_xml_parsed(full_address)
    api_xml_data = api_xml_parsed['api_parsed_data']
    sqft = api_xml_data.find('finishedSqFt').getText()

    return int(sqft)


