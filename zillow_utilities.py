import urllib
from bs4 import BeautifulSoup
from server import *


def format_api_url(full_address):
    """ Takes the address entered by user and returns a Zillow API encoded URL. """

    return 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=' + app.zwsid + '&' + urllib.urlencode(full_address)


def return_api_xml_parsed(full_address):
    """ Returns parsed XML data from Zillow's API. """

    api_url = format_api_url(full_address)
    api_xml = urllib.urlopen(api_url).read()
    api_xml_parsed = BeautifulSoup(api_xml, 'lxml-xml')
    api_response_code = api_xml_parsed.find('code').getText()

    return { 'api_response_code': api_response_code,
             'api_parsed_data': api_xml_parsed
           }


def get_unit_id(full_address):
    """ Scrapes unit_id from API response using BeautifulSoup. """

    api_xml_parsed = return_api_xml_parsed(full_address)
    api_xml_data = api_xml_parsed['api_parsed_data']

    # Checks for a valid xml response code
    if api_xml_parsed['api_response_code'] == 0:
        unit_id = api_xml_data.find('zpid').getText()
        return unit_id
    else:
        return None


def format_address(full_address):
    """ Takes the address entered by user and returns a URL-ready address with dashes. """

    address = full_address['address']
    city_state_zip = full_address['citystatezip']

    return address.replace(' ','-') + '-' + city_state_zip.replace(' ','-')


def return_html_parsed(full_address):
    """ Uses the unit id and formatted address to load and parse the HTML response. """

    unit_id = get_unit_id(full_address)
    formatted_full_address = format_address(full_address)

    # Using unit_id, finds unit listing page on Zillow
    zillow_page = 'http://www.zillow.com/homedetails/{}/{}_zpid/'.format(formatted_full_address, unit_id)
    zillow_url = urllib.urlopen(zillow_page).geturl()
    zillow_html = urllib.urlopen(zillow_url).read()

    return BeautifulSoup(zillow_html, 'lxml')


def get_unit_price(full_address):
    """ Extracts listing price of unit from Zillow. """

    zillow_html_parsed = return_html_parsed(full_address)

    try:
        # Check if there is a listing price on Zillow
        unit_price_string = str(zillow_html_parsed.find('div', class_='main-row home-summary-row').find('span'))
        unit_price = unit_price_string[unit_price_string.index('$') : unit_price_string.index(' <span class="value-suffix">')]
        return (100, unit_price)

    except AttributeError:
        # If unit is found off-market, look for a price estimate
        if get_zillow_price_estimate(full_address):
            zillow_price_estimate = int(get_zillow_price_estimate(full_address))
            return (200, 'We found that unit on the market, but it\'s currently not for sale. Zillow\'s estimated current market value of that unit is ${:,}'.format(zillow_price_estimate))
        # Otherwise unit is not found/address entered is incorrect
        else:
            return (300, 'Sorry, we couldn\'t find a unit with that listing address. Please try your search again.')


def get_zillow_price_estimate(full_address):
    """ Scrapes the Zillow price estimate if unit is not on the market. """

    api_xml_parsed = return_api_xml_parsed(full_address)

    # Checks for a valid xml response code
    if api_xml_parsed['api_response_code'] == 0:
        zillow_price_estimate = api_xml_parsed.find('amount').getText()

        return zillow_price_estimate
