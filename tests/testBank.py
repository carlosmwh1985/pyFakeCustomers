import unittest
import FakeCustomers.customers.bank as bank


class TestBankCustomer(unittest.TestCase):

    def setUp(self):
        self.bank0 = bank.BankCustomer()
        self.bank0.set_user()
        self.bank1 = bank.BankCustomer(
            client_locale='fr_FR', salutation='S', title='T',
            first_name='FN', last_name='LN', age='0',
            min_val=0, max_val=1, avg_credit=1000.0,
            max_num_cards=1, num_cards=2, num_visits=2, num_calls=3)
    
    def test_id(self):
        self.assertTrue(self.bank0.id, 'No Id was assigned')
        self.assertTrue(isinstance(self.bank0.id, int), 'Id is not an Integer')
        id_str = str(self.bank0.id)
        self.assertIs(7, len(id_str), 'The length of Id is not correct')

    def test_name(self):
        self.assertTrue(self.bank0.salutation, 'No Salutation assigned')
        self.assertTrue(self.bank0.first_name, 'No FirstName assigned')
        self.assertTrue(self.bank0.last_name, 'no LastName assigned')

    def test_address(self):
        self.assertTrue(self.bank0.address, 'No Address assigned')
        self.assertTrue(self.bank0.plz, 'No PostalCode assigned')
        self.assertTrue(self.bank0.city, 'No City assigned')
        self.assertTrue(self.bank0.phone, 'No Telephone Number assigned')
        self.assertIs('DE', self.bank0.country, 'The default country was not assigned')

    def test_age(self):
        self.assertTrue(self.bank0.age, 'No Age assigned')
        self.assertTrue(18 <= self.bank0.age < 99, 'Age is not in the expected range')

    def test_credit(self):
        self.assertTrue(self.bank0.credit_min <= self.bank0.credit < self.bank0.credit_max,
                        'Not the correct AvgCredit was calculated')
        self.assertTrue(self.bank0.num_cards <= self.bank0.max_num_cards,
                        'More NumCards than indicated were assigned')
        self.assertTrue(self.bank0.num_visits < 11,
                        'More NumVisits than indicated were assigned')
        self.assertTrue(self.bank0.num_online_visits < 20,
                        'More OnlineVisits than indicated were assigned')
        self.assertTrue(self.bank0.num_calls < 16,
                        'More NumCalls than indicated were assigned')

    def test_str(self):
        user_str = str(self.bank0)
        self.assertTrue(user_str.startswith('Bank Customer Name:'),
                        'String assignment is not the expected one')

    def test_custom_user(self):
        self.assertFalse(self.bank1.id, 'Defined customer has an Id')
        self.assertIs(self.bank1.salutation, 'S', 'Defined customer has the wrong Salutation')
        self.assertIs(self.bank1.title, 'T', 'Defined customer has the wrong Title')
        self.assertIs(self.bank1.first_name, 'FN', 'Defined customer has the wrong FirstName')
        self.assertIs(self.bank1.last_name, 'LN', 'Defined customer has the wrong LastName')
        self.assertIs(self.bank1.age, '0', 'Defined customer has the wrong Age')
        self.assertIsNot(self.bank1.country, 'DE', 'Defined customer has the wrong Country')
        self.assertIs(self.bank1.locale, 'fr_FR', 'Defined customer has the wrong Locale')
        self.assertIs(self.bank1.credit_min, 0, 'Defined customer has the wrong CreditMin')
        self.assertIs(self.bank1.credit_max, 1, 'Defined customer has the wrong CreditMax')
        self.assertIs(self.bank1.credit, 1000.0, 'Defined customer has the wrong AvgCredit')
        self.assertIs(self.bank1.max_num_cards, 1, 'Defined customer has the wrong MaxNumCards')
        self.assertIs(self.bank1.num_cards, 2, 'Defined customer has the wrong NumCards')
        self.assertIs(self.bank1.num_visits, 2, 'Defined customer has the wrong NumVisits')
        self.assertIs(self.bank1.num_calls, 3, 'Defined customer has the wrong NumCalls')

    def tearDown(self):
        del self.bank0
        del self.bank1
