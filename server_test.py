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


if __name__ == "__main__":

    unittest.main()
