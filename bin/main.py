import FakeCustomers.populateData.populate as populate
import json


def print_users(users):
    for user in users:
        print(json.dumps(user, indent=2))


def base_clients():
    faker = populate.FakerData(num_users=10)
    faker.create_list_users()
    fake_users = faker.get_list()
    print('Default users: ')
    print_users(fake_users)


def bank_clients():
    faker = populate.FakerData(num_users=10, type_users='bank')
    faker.create_list_users()
    fake_users = faker.get_list()
    print('\nBank users: ')
    print_users(fake_users)


if __name__ == '__main__':
    base_clients()
    bank_clients()
