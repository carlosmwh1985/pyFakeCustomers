import unittest
import FakeCustomers.customers.base as base


class TestDefaultCustomer(unittest.TestCase):

    def setUp(self):
        self.user0 = base.DefaultCustomer()
        self.user0.set_user()
        self.user1 = base.DefaultCustomer(
            client_locale='fr_FR', salutation='S', title='T',
            first_name='FN', last_name='LN', age='0')

    def test_id(self):
        self.assertTrue(self.user0.id, 'No Id was assigned')
        self.assertTrue(isinstance(self.user0.id, int), 'Id is not an Integer')
        id_str = str(self.user0.id)
        self.assertIs(7, len(id_str), 'The length of Id is not correct')

    def test_name(self):
        self.assertTrue(self.user0.salutation, 'No Salutation assigned')
        self.assertTrue(self.user0.first_name, 'No FirstName assigned')
        self.assertTrue(self.user0.last_name, 'no LastName assigned')

    def test_address(self):
        self.assertTrue(self.user0.address, 'No Address assigned')
        self.assertTrue(self.user0.plz, 'No PostalCode assigned')
        self.assertTrue(self.user0.city, 'No City assigned')
        self.assertTrue(self.user0.phone, 'No Telephone Number assigned')
        self.assertIs('DE', self.user0.country, 'The default country was not assigned')

    def test_age(self):
        self.assertTrue(self.user0.age, 'No Age assigned')
        self.assertTrue(18 <= self.user0.age < 99, 'Age is not in the expected range')

    def test_str(self):
        user_str = str(self.user0)
        self.assertTrue(user_str.startswith('Customer Name:'),
                        'String assignment is not the expected one')

    def test_custom_user(self):
        self.assertFalse(self.user1.id, 'Defined customer has an Id')
        self.assertIs(self.user1.salutation, 'S', 'Defined customer has the wrong Salutation')
        self.assertIs(self.user1.title, 'T', 'Defined customer has the wrong Title')
        self.assertIs(self.user1.first_name, 'FN', 'Defined customer has the wrong FirstName')
        self.assertIs(self.user1.last_name, 'LN', 'Defined customer has the wrong LastName')
        self.assertIs(self.user1.age, '0', 'Defined customer has the wrong Age')
        self.assertIsNot(self.user1.country, 'DE', 'Defined customer has the wrong Country')
        self.assertIs(self.user1.locale, 'fr_FR', 'Defined customer has the wrong Locale')

    def tearDown(self):
        del self.user0
        del self.user1
