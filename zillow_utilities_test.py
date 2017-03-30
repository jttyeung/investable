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


    def test_get_api_xml(self):
        # Mock an API response parsed by BeautifulSoup
        self.mock_api_xml = open(self.mock_file_content).read()
        self.assertEqual(self.mock_api_xml, get_api_xml(self.mock_address))


    def test_parse_xml(self):
        parsed_xml = parse_xml(self.mock_address)
        self.assertEqual(0, parsed_xml['api_response_code'])


    def test_get_zillow_html_url(self):
        self.assertEqual('http://www.zillow.com/homedetails/151-Bacardi-Ave-San-Francisco-CA-94109/11111111_zpid/', get_zillow_html_url(self.mock_address))


    def parse_html(self):
        pass


    def test_get_unit_price(self):
        self.assertEqual((100, '$1,500,500'), get_unit_price(self.mock_address))


    def test_get_zillow_price_estimate(self):
        self.assertEqual('1395020',get_zillow_price_estimate(self.mock_address))


    def test_get_zillow_unit_details(self):
        self.assertEqual({'neighborhood': 'Tenderloin',
                          'latlng_point': 'POINT(37.729981 -122.452644)',
                          'bedrooms': '3',
                          'bathrooms': '2.5',
                          'sqft': '1386'
                        }, get_zillow_unit_details(self.mock_address))


    def tearDown(self):
        """ Tear down at end of each test. """
        pass



if __name__ == "__main__":
    unittest.main()
