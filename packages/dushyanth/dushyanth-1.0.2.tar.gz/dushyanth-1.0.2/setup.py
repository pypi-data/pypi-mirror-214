from setuptools import setup

setup(
    name='dushyanth',
    version='1.0.2',
    description='This code will find if a given IP is allowed in a AWS security group rule for a given instance with name tag available',
    author='Dushyanth Boppidi',
    packages=['find_ip_to_db'],
    install_requires=['boto3', 'ipaddress', 'sqlite3'],
)
