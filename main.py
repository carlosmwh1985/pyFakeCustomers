from src.populateData.populate import FakerData


def base_clients():
    faker = FakerData(num_users=10)
    faker.create_list_users()
    fake_users = faker.get_list()
    print('Default users: ' + fake_users)


def bank_clients():
    faker = FakerData(num_users=10, type_users='bank')
    faker.create_list_users()
    fake_users = faker.get_list()
    print('Bank users: ' + fake_users)


if __name__ == '__main__':
    base_clients()
    bank_clients()
