#! /usr/bin/env python
import os
from setuptools import setup
from finitelycomputable_microsites_setup import (
        version, base_setup, wsgi_extras_require, falcon_version,
)

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
    long_description_content_type="text/x-rst",
    scripts=['finitelycomputable_microsites_setup.py'],
    install_requires=[falcon_version],
    extras_require=wsgi_extras_require,
    url='http://www.finitelycomputable.net/hello_world/',
    **base_setup
)
