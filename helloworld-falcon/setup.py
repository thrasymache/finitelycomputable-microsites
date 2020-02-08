#! /usr/bin/env python
import os
from setuptools import setup
from finitelycomputable_microsites_setup import version, base_setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='finitelycomputable-helloworld-falcon',
    version=version,
    py_modules=['finitelycomputable.helloworld_falcon'],
    entry_points={
        'console_scripts': [
            'finitelycomputable-helloworld-falcon = finitelycomputable.helloworld_falcon:run']
        },
    description='A hello_world implementation in Falcon',
    long_description=README,
    scripts=['finitelycomputable_microsites_setup.py'],
    install_requires=['falcon~=2.0'],
    extras_require={
        'bjoern': ['bjoern<4'],
        'cheroot': ['cheroot<9'],
        'cherrypy': ['cherrypy<19'],
        'gunicorn': ['gunicorn<20'],
        'waitress': ['waitress<1.4'],
        },
    url='https://www.finitelycomputable.net/hello_world/',
    **base_setup
)
