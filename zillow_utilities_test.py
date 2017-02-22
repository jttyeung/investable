import unittest
import os
from zillow_utilities import *


class ZillowTests (unittest.TestCase):
    """ Unit testing for zillow_utilities. """


    def setUp(self):
        """ Setup before each test. """
        self.maxDiff = None
        # Get the Flask test client
        self.client = app.test_client()

        self.mock_file_content = 'mock_zillow_api_xml_parsed.html'

        # Mock an address
        self.current_script_directory = os.path.dirname(os.path.realpath(__file__))
        self.mock_address = 'file://' + self.current_script_directory + '/' + self.mock_file_content


        # self.mock_api_xml_parsed = BeautifulSoup(self.mock_api_xml, 'lxml-xml')
        self.mock_api_response_code = 0


    def test_format_api_url(self):
        # Mock an address
        self.mock_address = {'address': '151 Bacardi Ave.', 'citystatezip': 'san francisco ca' }

        self.assertEqual('http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=' + app.zwsid + '&citystatezip=san+francisco+ca&address=151+Bacardi+Ave.', format_api_url(self.mock_address))


    def test_return_api_xml(self):
        # Mock an API response parsed by BeautifulSoup
        self.mock_api_xml = open(self.mock_file_content).read()
        self.assertEqual(self.mock_api_xml, return_api_xml(self.mock_address))


    def test_parse_xml(self):
        parsed_xml = parse_xml(self.mock_address)
        self.assertEqual(0, parsed_xml['api_response_code'])


    # def get_zillow_html_page(self):
    #     pass


    # def return_html_parsed(self):
    #     pass


    def test_get_unit_price(self):
        self.assertEqual((100, '$1,500,500'), get_unit_price(self.mock_address))
        # self.assertEqual((200, 'We found the unit you were searching for, but it\'s not currently for sale. Zillow\'s estimated current market value of that unit is $1395020), get_unit_price())
        # self.assertEqual('(300, 'Sorry, we couldn't find a unit with that listing address. Please try your search again.')', get_unit_price())


    # def test_get_zillow_price_estimate(self):
    #     self.assertEqual('1035000', get_zillow_price_estimate(self.test_return_api_xml_parsed()))


    # def test_get_neighborhood(full_address):
    #     self.assertEqual('Tenderloin', get_neighborhood())


    # def test_get_latlong(full_address):
    #     self.assertEqual('POINT(37.729981 122.452644)', get_latlong())


    # def test_get_bedrooms(full_address):
    #     self.assertEqual(3, get_bedrooms())


    # def test_get_bathrooms(full_address):
    #     self.assertEqual(2.5, get_bathrooms())


    # def get_sqft(full_address):
    #     self.assertEqual(1386, get_sqft())


    def tearDown(self):
        """ Tear down at end of each test. """
        pass



if __name__ == "__main__":
    unittest.main()
