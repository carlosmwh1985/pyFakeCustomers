import numpy as np

from ..customers.base import DefaultCustomer
from ..customers.bank import BankCustomer


def fill_indices(fraction, total_number):
    total_number: int
    num_indices = max(0, int(fraction * total_number))
    return np.random.randint(0, total_number, num_indices)


class FakerData:
    """It constructs a list of fake users, of the given type (standard/base, bank...),
    and save them in a list. The number of outliers can be defined.

    Arguments:\n
    num_users  : the number of clients to create. 100, by default\n
    type_users : the type of user. 'base' for the standard one, 'bank' for a bank client\n\n

    Optional keyword arguments:\n
    frac_nans  : the fraction of num_users will have some NaNs / invalid data\n
    credit_min : for 'bank' customer, the minimum value for the credit card limit average\n
    credit_max : for 'bank' customer, the maximum value for the credit card limit average\n
    max_cards  : for 'bank' customer, the maximum number of credit cards. By default it is set to 10\n
    frac_out   : the fraction of num_users will have outliers in any of random-generated numeric values.\n
                 The eligible columns are configured according type_users.\n
    error      : The deviation of the outliers from the mean value
    """

    def __init__(self, num_users=100, type_users='base', **kwargs):
        # Read inputs
        self.num_users = num_users
        self.type_users = type_users

        # Initialize variables
        self._clear_lists()

        # Initial configurations
        self._extract_args(kwargs)
        self._set_faker()
        self._config_invalid()
        self._config_outliers()

    def _clear_lists(self):
        self.indices_nan = []
        self.indices_out = []
        self.faked_users = []
        self.tmp_ids = set()
        self.nan_cols = []
        self.out_cols = []
        self.user_data = {}
        self.max_min = {}

    def _clear_user_data(self):
        self.user_data = {}

    def _extract_args(self, kwargs):
        # Bank customer related parameters
        self.credit_min = kwargs.get('credit_min', 0)
        self.credit_max = kwargs.get('credit_max', 1)
        self.max_num_cards = kwargs.get('max_cards', 10)

        # Invalid data related params
        self.frac_nans = kwargs.get('frac_nans', 0.0)

        # Outlier generator related parameters
        self.frac_out = kwargs.get('frac_out', 0.0)
        self.error = kwargs.get('error', 0.0)

    def _set_faker(self):
        if self.type_users == 'base':
            self.user = DefaultCustomer()
            self.nan_cols = ['Address', 'Phone', 'Age']
        elif self.type_users == 'bank':
            self.user = BankCustomer(min_val=self.credit_min, max_val=self.credit_max,
                                     max_num_cards=self.max_num_cards)
            self.nan_cols = ['Avg_Credit_Limit', 'Total_Credit_Cards',
                             'Total_Visits_Bank', 'Total_Visits_Online',
                             'Total_Calls_Made']
            self.out_cols = ['Avg_Credit_Limit']
            self.max_min['Avg_Credit_Limit.max'] = self.credit_max
            self.max_min['Avg_Credit_Limit.min'] = self.credit_min

    def _config_invalid(self):
        """Set the number of rows with NaNs/Invalid data and choose the indices of the rows randomly"""
        if self.frac_nans > 0:
            self.indices_nan = fill_indices(self.frac_nans, self.num_users)
            self.num_nans = self.indices_nan.size

    def _config_outliers(self):
        """Set the number of rows with outliers and choose the indices of the rows randomly"""
        if self.frac_out > 0:
            self.indices_out = fill_indices(self.frac_out, self.num_users)
            self.num_outliers = self.indices_out.size

    def _put_a_nan(self):
        # Throw a dice, to see how many NaNs will be given
        num_nans = np.random.randint(len(self.nan_cols)) + 1

        # Create the NaNs
        for i in range(num_nans):
            col_name = np.random.choice(self.nan_cols)
            if self.user_data[col_name] is not None:
                self.user_data[col_name] = None

    def _modify_data(self):
        if not self.num_outliers or self.num_outliers < 1:
            return

        for col in self.out_cols:
            # Random values to calculate a random outlier
            val0 = self.user_data[col]
            sign = np.random.choice((1, -1))
            seed = np.random.random_sample()

            # Get the reference values
            min_val = self.max_min[col + '.min']
            max_val = self.max_min[col + '.max']
            mean_val = (max_val - min_val) / 2.

            # Calculate the outlier
            new_val = max(min_val, val0 + sign * (mean_val + self.error * seed))
            new_val = min(max_val, new_val)
            self.user_data[col] = new_val

    def create_fake_user(self):
        """Calls the instance of Customer and save the random generated customer in `user_data`"""
        # Initialize
        self._clear_user_data()
        self.user.set_user()

        # Populate
        self.user_data['User_ID'] = self.user.id
        self.user_data['Salutation'] = self.user.salutation
        self.user_data['Title'] = self.user.title
        self.user_data['FirstName'] = self.user.first_name
        self.user_data['LastName'] = self.user.last_name
        self.user_data['Gender'] = self.user.gender
        self.user_data['Age'] = self.user.age
        self.user_data['Address'] = self.user.address
        self.user_data['PLZ'] = self.user.plz
        self.user_data['City'] = self.user.city
        self.user_data['PhoneNumber'] = self.user.phone

        if self.type_users == 'bank':
            self.user_data['Avg_Credit_Limit'] = round(self.user.credit, 2)
            self.user_data['Total_Credit_Cards'] = self.user.num_cards
            self.user_data['Total_Visits_Bank'] = self.user.num_visits
            self.user_data['Total_Visits_Online'] = self.user.num_online_visits
            self.user_data['Total_Calls_Made'] = self.user.num_calls

    def create_list_users(self):
        """Creates a list of Users/Customers, of the size specified in `num_users`, of `type_users` type.
        It also adds NaNs and Outliers, if `frac_nans` and `frac_out` are given."""
        # Loop to create the fake data
        i = 0
        while i < self.num_users:
            # Create a Fake User, with random Data
            self.create_fake_user()
            if self.user.id not in self.tmp_ids:
                self.tmp_ids.add(self.user.id)

                # Insert NaNs and outliers in random positions (previously selected)
                if i in self.indices_out:
                    self._modify_data()
                elif i in self.indices_nan:
                    self._put_a_nan()

                # Save self.user_data into list
                self.faked_users.append(self.user_data)

                i += 1

    def get_list(self):
        return self.faked_users


if __name__ == '__main__':
    faker = FakerData(num_users=10)
    faker.create_list_users()
    fake_users = faker.get_list()
    print('Default users: ' + fake_users)

    faker = FakerData(num_users=10, type_users='bank')
    faker.create_list_users()
    fake_users = faker.get_list()
    print('Bank users: ' + fake_users)
