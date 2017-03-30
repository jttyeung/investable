import unittest
from flask import session
import server
from model import *
from server import app


class FlaskServerIntegrationTests(unittest.TestCase):
    """ Integration testing for Investable's server. """


    def setUp(self):
        """ Sets up a new client test app before each test. """

        self.client = app.test_client()
        app.config['TESTING'] = True


    def test_homepage(self):
        """ Test that the homepage route loads. """

        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        # import pdb; pdb.set_trace()
        self.assertIn('<h1>Find rental property real estate that is <span id="appname">Investable</span>.', result.data)
        self.assertIn('Search Again', result.data)


    def test_search(self):
        """ Test that the search route returns a response. """

        app.zwsid = app.zwsid
        result = self.client.get('/search.json')
        self.assertEqual(result.status_code, 200)


    # def test_avg_rent(self):
    #     """ Test that the average rent route returns a response. """

    #     result = self.client.get('/avgrent.json')
    #     self.assertEqual(result.status_code, 200)


    # def test_listings(self):
    #     """ Test that the listings route returns a response. """

    #     result = self.client.get('/listings.json')
    #     self.assertEqual(result.status_code, 200)


    # def test_calculator(self):
    #     """ Test that the calculator route returns a response. """

    #     result = self.client.get('/calculator')
    #     self.assertEqual(result.status_code, 200)


    # def test_login(self):
    #     """ Test that the login page loads. """

    #     result = self.client.post('/login',
    #                               data={'user_id': 'glindagood@example.com', 'password': 'glinda'},
    #                               follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)


    # def test_register(self):
    #     """ Test that the registration page loads. """

    #     result = self.client.get('/register')
    #     self.assertEqual(result.status_code, 200)


    # def test_registration_success(self):
    #     """ Test that the user is able to successfully register. """
    #     result = self.client.post('/register',
    #         data={'user_id': 'nessarosethropp@example.com', 'password': '12345'},
    #         follow_redirects=True)
    #     self.assertEqual(result.status_code, 200)


    # def test_registration_invalid(self):
    #     """ Test that the user cannot create an account if it already exists in the database. """
    #     result = self.client.post('/register')
    #     self.assertEqual(result.status_code, 200)
    #     # add assertIn


    # def test_account_details(self):
    #     """ Test that user account detail page loads. """
    #     result = self.client.get('/account')
    #     self.assertEqual(result.status_code, 200)



class FlaskDatabaseTests(unittest.TestCase):
    """ Flask tests that use the database. """

    def setUp(self):
        """ Sets up a new client test app and database before each test. """
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db_flask(app, 'postgresql:///testdb')

        # Create tables and add sample data
        db.create_all()
        sample_data()


    def tearDown(self):
        """Drop database after every test."""

        db.session.close()
        db.drop_all()


    def test_user(self):
        """ Make sure we can find a user. """

        glinda = User.query.filter(User.firstname == 'glinda').first()
        self.assertEqual('glinda', glinda.firstname)
        self.assertEqual('glindagood@example.com', glinda.email)


    def test_listing(self):
        """ Make sure we can find a listing. """

        listing = Listing.query.get(38478998)
        self.assertEqual(38478998, listing.zpid)
        self.assertEqual(350, listing.hoa)
        self.assertEqual(980430, listing.price)


    def test_unit_details(self):
        """ Make sure we can find unit details. """

        listing = Listing.query.get(38478998)
        self.assertEqual(2.0, listing.unitdetails.bedrooms)
        self.assertEqual(1190, listing.unitdetails.sqft)
        self.assertEqual(37.7872375, listing.unitdetails.latitude)


    def test_rentals(self):
        """ Make sure we can find a rental. """

        rental = Rental.query.filter(Rental.cl_id == '6007117642').first()
        self.assertEqual(1885, rental.price)


    # def test_get_avg_rent(self):
    #     """Test rent averages."""

    #     self.mock_bedrooms = 2
    #     self.mock_bathrooms = 2
    #     self.mock_sqft = 2000
    #     self.mock_latlng_point = 'POINT(37.8212167 -122.4211727)'

    #     self.assertEqual({ 'avg_rent_by_br': 4468, 'avg_rent_by_sqft': 6080 }, get_avg_rent(self.mock_bedrooms, self.mock_bathrooms, self.mock_sqft, self.mock_latlng_point))


   # def test_add_listing_to_db(self):
   #      """Test rent averages."""

   #      self.mock_bedrooms = 3
   #      self.mock_bathrooms = 2
   #      self.mock_sqft = 2200
   #      self.mock_zpid = 33039402
   #      self.mock_street = '209 Yellow Brick Rd'
   #      self.mock_city = 'Emerald City'
   #      self.mock_state = 'EA'
   #      self.mock_zipcode = 93240
   #      self.mock_latitude = 37.7791402
   #      self.mock_longitude = -122.5659901
   #      self.mock_price = 1420975
   #      self.mock_hoa = 550

   #      self.assertEqual({ 'avg_rent_by_br': 4468, 'avg_rent_by_sqft': 6080 }, add_listing_to_db(self.mock_bedrooms, self.mock_bathrooms, self.mock_sqft, self.mock_latitude, self.mock_longitude, self.mock_price, self.mock_zpid, self.mock_street, self.mock_city, self.mock_state, self.mock_zipcode, self.mock_hoa))






if __name__ == "__main__":

    unittest.main()
