import unittest
import server

class InvestableServerTest(unittest.TestCase):
    """ Integration testing for Investable's server. """


    def setUp(self):
        """ Sets up new test client per test. """
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True


    def test_homepage(self):
        """ Test that the homepage loads. """
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)
        # add assertIn


    def test_login(self):
        """ Test that the login page loads. """
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        # add assertIn


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


if __name__ == '__main__':
    unittest.main()
