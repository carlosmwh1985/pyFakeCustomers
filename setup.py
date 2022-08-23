from setuptools import setup, find_packages


setup(
    name='FakeCustomers',
    version='0.1.1',
    package_dir={"": "src"},
    packages=find_packages('src'),
    url='',
    license='MIT',
    author='Carlos Granados',
    author_email='carlosm.granadosc@gmail.com',
    description='A package to create fake customers'
)