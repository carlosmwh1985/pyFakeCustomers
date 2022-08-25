import unittest
import pandas as pd
import FakeCustomers.populateData.populate as populate
from FakeCustomers.customers.base import DefaultCustomer
from FakeCustomers.customers.bank import BankCustomer


class TestPopulateDate(unittest.TestCase):

    def test_DefaultCustomer_creation(self):
        creator = populate.FakerData()
        creator.create_fake_user()
        self.assertTrue(isinstance(creator.user, DefaultCustomer))
        self.assertIs(creator.credit_min, 0, 'Not the expected CreditMin')
        self.assertIs(creator.credit_max, 1, 'Not the expected CreditMax')
        self.assertIs(int(creator.frac_nans), 0, 'Not the expected FracNans')
        self.assertIs(int(creator.frac_out), 0, 'Not the expected FracOut')
        self.assertIs(int(creator.error), 0, 'Not the expected Outliers-Error')

    def test_BankCustomer_creation(self):
        creator = populate.FakerData(type_users='bank')
        creator.create_fake_user()
        self.assertTrue(isinstance(creator.user, BankCustomer))

    def test_DefaultCustomers(self):
        creator = populate.FakerData(num_users=57)
        creator.create_list_users()
        users = creator.get_list()
        self.assertTrue(len(users) == 57, 'Not the expected number of users')

    def test_nan_arguments(self):
        num_users = 1000
        frac_nans = 0.25
        num_nans = int(num_users * frac_nans)
        creator = populate.FakerData(num_users=num_users, frac_nans=frac_nans)
        self.assertIs(creator.num_nans, num_nans, 'Not the expected number of NaNs')

    def test_nan_creation(self):
        num_users = 1000
        frac_nans = 0.25
        num_nans = int(num_users * frac_nans)
        creator = populate.FakerData(num_users=num_users, frac_nans=frac_nans,
                                     type_users='bank')
        creator.create_list_users()
        users = creator.get_list()
        df = pd.DataFrame(users)
        num_nans_data = df.shape[0] - df.dropna().shape[0]
        self.assertIs(creator.num_nans, num_nans, 'Not the expected number of NaNs')
        self.assertIs(len(creator.indices_nan), num_nans, 'Not the expected number of indices')
        self.assertIs(num_nans_data, num_nans, 'Not the expected number of rows with NaNs')
        #TODO: Check why this test is failing!

    def test_outliers_conf(self):
        num_users = 1000
        frac_out = 0.25
        error = 1597.7531
        num_outs = int(num_users * frac_out)
        creator = populate.FakerData(num_users=num_users, frac_out=frac_out,
                                     error=error, type_users='bank')
        self.assertIs(creator.num_outliers, num_outs, 'Not the expected number of NaNs')
        self.assertIs(len(creator.indices_out), num_outs, 'Not the expected number of indices')
        self.assertIs(creator.error, error, 'Not the expected value for the error')

