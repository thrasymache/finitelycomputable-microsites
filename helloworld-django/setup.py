#! /usr/bin/env python
import os
from setuptools import setup
from finitelycomputable_microsites_setup import (
        version, django_setup, wsgi_extras_require,
)

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='finitelycomputable-helloworld-django',
    version=version,
    packages=['finitelycomputable.helloworld_django'],
    entry_points={
        'console_scripts': [
            'finitelycomputable-helloworld-django = finitelycomputable.helloworld_django:run']
        },
    description='A hello_world implementation in Django',
    long_description=README,
    long_description_content_type="text/x-rst",
    scripts=['finitelycomputable_microsites_setup.py'],
    install_requires=['Django~=3.0'],
    extras_require=wsgi_extras_require,
    url='http://www.finitelycomputable.net/hello_world',
    **django_setup
)
