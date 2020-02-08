#! /usr/bin/env python
import os
from setuptools import setup
from finitelycomputable_microsites_setup import version, base_setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='finitelycomputable-helloworld-flask',
    version=version,
    py_modules=['finitelycomputable.helloworld_flask'],
    entry_points={
        'console_scripts': [
            'finitelycomputable-helloworld-flask = finitelycomputable.helloworld_flask:run']
        },
    description='A hello_world implementation in Flask',
    long_description=README,
    scripts=['finitelycomputable_microsites_setup.py'],
    install_requires=['Flask~=1.1'],
    url='https://www.finitelycomputable.net/identification_of_trust',
    **base_setup
)
