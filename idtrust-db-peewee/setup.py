#! /usr/bin/env python
import os
from setuptools import find_namespace_packages, setup
from finitelycomputable_microsites_setup import (
        version, base_setup, wsgi_extras_require, peewee_version,
)

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='finitelycomputable-idtrust-db-peewee',
    version=version,
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': []
        },
    description='Peewee implementation of database layer for the Identification of Trust microsite',
    long_description=README,
    long_description_content_type="text/x-rst",
    scripts=['finitelycomputable_microsites_setup.py'],
    install_requires=[
       peewee_version,
        ],
    url='http://www.finitelycomputable.net/identification_of_trust',
    **base_setup
)
