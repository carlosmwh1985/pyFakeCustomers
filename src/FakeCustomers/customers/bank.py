import numpy as np
from base import DefaultCustomer


class BankCustomer(DefaultCustomer):
    """It creates a fake bank customer, with a random number
    of active credit cards and a random credit average"""

    def __init__(self, min_val=3000.0, max_val=500000.0, max_num_cards=10,
                 avg_credit=0, num_cards=0, num_visits=0, num_online_visits=0, num_calls=0,
                 client_locale='de_DE', country=None,
                 salutation=None, title=None, first_name=None, last_name=None,
                 age=None, address=None, plz=None, city=None, phone=None,
                 **kwargs):

        # Initialize super
        super(BankCustomer, self).__init__(
            client_locale=client_locale, country=country,
            salutation=salutation, title=title, first_name=first_name, last_name=last_name,
            age=age, address=address, plz=plz, city=city, phone=phone,
            kwargs=kwargs)

        # Save arguments
        self.credit_min = min_val
        self.credit_max = max_val
        self.max_num_cards = max_num_cards

        # Initialize variables
        self._bank_start(avg_credit, num_cards, num_visits, num_online_visits, num_calls)

    def _bank_start(self, credit, cards, visits, online_visits, calls):
        self.num_cards = cards
        self.credit = credit
        self.num_visits = visits
        self.num_online_visits = online_visits
        self.num_calls = calls

    def _user_credit_avg(self):
        delta = self.credit_max - self.credit_min
        val = np.random.random_sample()
        self.credit = delta * val + self.credit_min

    def _user_num_cards(self):
        self.num_cards = np.random.randint(1, self.max_num_cards+1)
        # TODO: set limits for number of cards

    def _user_num_visits(self):
        self.num_visits = np.random.randint(0, 11)
        self.num_online_visits = np.random.randint(0, 21)
        self.num_calls = np.random.randint(0, 16)

    def __str__(self):
        name = f'{self.salutation} {self.title} {self.first_name} {self.last_name}'
        credit_info = f'Avg. Credit {round(self.credit, 2)}, Num. Credit Cards: {self.num_cards}'
        return 'Bank Customer Name: ' + name + '\nCredit Information: ' + credit_info

    def __repr__(self):
        return f'BankCustomer(salutation={self.salutation}, title={self.title}, first_name={self.first_name},' \
               f' last_name={self.last_name}, avg_credit={self.credit}, num_cards={self.num_cards},' \
               f' address={self.address}, plz={self.plz}, city={self.city}, self.phone={self.phone},' \
               f' country={self.country}, client_locale={self.locale})'

    def set_user(self):
        super().set_user()
        self._user_credit_avg()
        self._user_num_cards()
        self._user_num_visits()


if __name__ == '__main__':
    test_customer = BankCustomer()
    test_customer.set_user()
    print(test_customer)




