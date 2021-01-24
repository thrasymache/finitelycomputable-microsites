#! /usr/bin/env python
import os
from setuptools import setup
from finitelycomputable_microsites_setup import (
        version, base_setup, wsgi_extras_require, morepath_version,
)

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='finitelycomputable-helloworld-morepath',
    version=version,
    py_modules=['finitelycomputable.helloworld_morepath'],
    entry_points={
        'console_scripts': [
            'finitelycomputable-helloworld-morepath = finitelycomputable.helloworld_morepath:run']
        },
    description='A hello_world implementation in Morepath',
    long_description=README,
    long_description_content_type="text/x-rst",
    scripts=['finitelycomputable_microsites_setup.py'],
    install_requires=[morepath_version],
    extras_require=wsgi_extras_require,
    url='http://www.finitelycomputable.net/hello_world/',
    **base_setup
)
