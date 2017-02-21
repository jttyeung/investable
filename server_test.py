import unittest
from flask import session

from model import connect_to_db_flask, db, sample_data
from server import app


class FlaskServerIntegrationTests(unittest.TestCase):
    """ Integration testing for Investable's server. """


    def setUp(self):
        """ Sets up a new client test app before each test. """
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """ Test that the homepage loads. """
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Search a property by location or city:', result)

    # what should this test? is this a functional test instead?
    def test_search(self):
        """ Test that the search element returns a response. """
        result = self.client.get('/search')
        self.assertEqual(result.status_code, 200)
        # add assertIn

    def test_login(self):
        """ Test that the login page loads. """
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        # add assertIn

    # # move to functional tests
    # def test_login(self):
    #     """ Test that the user is able to login. """
    #     result = self.client.post('/login')
    #     self.assertEqual(result.status_code, 200)
    #     # add assertIn

    def test_register(self):
        """ Test that the registration page loads. """
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 200)
        # add assertIn

    # def test_registration_success(self):
    #     """ Test that the user is able to successfully register. """
    #     result = self.client.post('/register')
    #     self.assertEqual(result.status_code, 200)
    #     # add assertIn

    # def test_registration_invalid(self):
    #     """ Test that the user cannot create an account if it already exists in the database. """
    #     result = self.client.post('/register')
    #     self.assertEqual(result.status_code, 200)
    #     # add assertIn

    def test_account_details(self):
        """ Test that user account detail page loads. """
        result = self.client.get('/account')
        self.assertEqual(result.status_code, 200)
        # add assertIn


class FlaskDatabaseTests(unittest.TestCase):
    """ Flask tests that use the database. """

    def setUp(self):
        """ Sets up a new client test app and database before each test. """

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        sample_data()

    def tearDown(self):
        """Drop database after every test."""

        db.session.close()
        db.drop_all()

    def test_rent_avgs(self):
        """Test rent averages."""

        result = self.client.get('/search.json')
        # self.assertIn('', result.data)
        return 'fail'

    def test_login(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"user_id": "glindagood@example.com", "password": "12345"},
                                  follow_redirects=True)
        # self.assertIn('', result.data)
        return 'fail'

    def test_registration(self):
        """Test registration page."""

        result = self.client.post("/register",
                                  data={"user_id": "nessarosethropp@example.com", "password": "12345"},
                                  follow_redirects=True)
        # self.assertIn('', result.data)
        return 'fail'




if __name__ == '__main__':
    unittest.main()
