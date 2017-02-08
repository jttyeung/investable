import urllib
from bs4 import BeautifulSoup
from server import *


def format_address(full_address):
    """ Takes the address entered by user and returns a URL-ready address with dashes. """

    address = full_address['address']
    city_state_zip = full_address['citystatezip']
    return address.replace(' ','-') + '-' + city_state_zip.replace(' ','-')


def format_api_url(full_address):
    """ Takes the address entered by user and returns a Zillow API encoded URL. """

    return 'http://www.zillow.com/webservice/GetSearchResults.htm?zws-id=' + app.zwsid + '&' + urllib.urlencode(full_address)


def get_unit_id(full_address):
    """ Scrapes unit_id from API response using BeautifulSoup. """

    api_url = format_api_url(full_address)
    api_xml = urllib.urlopen(api_url).read()
    api_parsed = BeautifulSoup(api_xml, 'lxml-xml')
    unit_id = api_parsed.find('zpid').getText()

    return unit_id


def get_unit_price(full_address):
    """ Gets listing price of unit on Zillow. """

    unit_id = get_unit_id(full_address)
    formatted_full_address = format_address(full_address)

    # Using unit_id, finds unit listing page on Zillow
    zillow_page = 'http://www.zillow.com/homedetails/{}/{}_zpid/'.format(formatted_full_address, unit_id)
    zillow_url = urllib.urlopen(zillow_page).geturl()
    zillow_html = urllib.urlopen(zillow_url).read()
    zillow_soup = BeautifulSoup(zillow_html, 'lxml')

    # Extracts unit's listing price from Zillow's DOM
    unit_price_string = str(zillow_soup.find('div', class_='main-row home-summary-row').find('span'))
    unit_price = unit_price_string[unit_price_string.index('$') : unit_price_string.index(' <span class="value-suffix">')]

    return unit_price
