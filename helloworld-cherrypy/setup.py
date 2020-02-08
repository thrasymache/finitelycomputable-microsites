#! /usr/bin/env python
import os
from setuptools import setup
from finitelycomputable_microsites_setup import version, base_setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='finitelycomputable-helloworld-cherrypy',
    version=version,
    py_modules=['finitelycomputable.helloworld_cherrypy'],
    entry_points={
        'console_scripts': [
            'finitelycomputable-helloworld-cherrypy = finitelycomputable.helloworld_cherrypy:run']
        },
    description='A hello_world implementation in CherryPy',
    long_description=README,
    scripts=['finitelycomputable_microsites_setup.py'],
    install_requires=['CherryPy<19'],
    url='https://www.finitelycomputable.net/hello_world',
    **base_setup
)
