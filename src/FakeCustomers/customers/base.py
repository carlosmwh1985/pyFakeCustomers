import numpy as np
from faker import Faker


class DefaultCustomer:
    """Class to create a default fake customer. It only includes
    the most relevant data.

    By default, the locale settings are set to Germany. They can
    be by initializing the class with a different value for
    client_locale."""

    def __init__(self, client_locale='de_DE', country=None,
                 salutation=None, title=None, first_name=None, last_name=None,
                 age=None, address=None, plz=None, city=None, phone=None,
                 **kwargs):
        self.locale = client_locale
        self.genders = ['F', 'M', 'X']
        self.faker = Faker(self.locale)
        self._start(salutation, title, first_name, last_name,
                    age, address, plz, city, country, phone)

    def _start(self, salutation, title, first_name, last_name,
               age, address, plz, city, country, phone):
        self.id = None
        self.gender = None
        self.salutation = salutation
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.address = address
        self.plz = plz
        self.city = city
        if country:
            self.country = country
        else:
            self.country = self.locale.split('_')[1]
        self.phone = phone

    def _user_id(self):
        """Create a random ID (int), with 7 digits"""
        self.id = np.random.randint(1000000, 10000000)

    def _user_age(self):
        self.age = np.random.randint(18, 99)

    def _user_gender(self):
        self.gender = np.random.choice(self.genders)

    def _user_salutation(self):
        if not self.gender:
            self._user_gender()

        if self.gender == 'F':
            self.salutation = 'Frau'
        elif self.gender == 'M':
            self.salutation = 'Herr'
        else:
            self.salutation = 'Mx.'

    def _user_title(self):
        dice = np.random.choice([0, 1])
        if dice:
            if self.gender == 'F':
                self.title = self.faker.prefix_female()
            elif self.gender == 'M':
                self.title = self.faker.prefix_male()
            else:
                self.title = self.faker.prefix()

            if self.title in ['Herr', 'Frau']:
                self._user_title()
        else:
            self.title = ''

    def _user_first_name(self):
        if self.gender == 'F':
            self.first_name = self.faker.first_name_female()
        elif self.gender == 'M':
            self.first_name = self.faker.first_name_male()
        else:
            self.first_name = self.faker.first_name_nonbinary()

    def _user_name(self):
        if not self.gender:
            self._user_gender()

        self._user_title()
        self._user_first_name()
        self.last_name = self.faker.last_name()

    def _user_address(self):
        tmp = self.faker.address()
        comps = tmp.split('\n')
        # if len(comps) != 2:
        #     raise AddressException('todo')

        city = comps[1].split(' ')
        self.address = comps[0]
        self.plz = str(city[0])
        self.city = city[1]
        self.country = 'DE'

    def _user_phone(self):
        self.phone = self.faker.phone_number()
        # TODO: Check that the number corresponds to the city

    def __str__(self):
        return f'Customer Name: {self.salutation} {self.title} {self.first_name} {self.last_name}'

    def __repr__(self):
        return f'DefaultCustomer(salutation={self.salutation}, title={self.title}, first_name={self.first_name}, last_name={self.last_name}'

    def set_user(self):
        self._user_id()
        self._user_salutation()
        self._user_name()
        self._user_age()
        self._user_address()
        self._user_phone()

    __set_user = set_user
    __start = _start


if __name__ == '__main__':
    test_customer = DefaultCustomer()
    test_customer.set_user()
    print(test_customer)
