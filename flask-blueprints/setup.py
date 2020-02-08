#! /usr/bin/env python
import os
from setuptools import setup
from finitelycomputable_microsites_setup import version, base_setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='finitelycomputable-flask-blueprints',
    version=version,
    py_modules=['finitelycomputable.flask_blueprints'],
    entry_points={
        'console_scripts': [
            'finitelycomputable-flask-blueprints = finitelycomputable.flask_blueprints:run']
        },
    description='The Flask-based wsgi app using blueprints to combine the microsites of finitelycomputable.net',
    long_description=README,
    scripts=['finitelycomputable_microsites_setup.py'],
    install_requires=['Flask~=1.1'],
    extras_require={
        'helloworld': ['finitelycomputable-helloworld-flask~=' + version],
        'bjoern': ['bjoern<4'],
        'cheroot': ['cheroot<9'],
        'cherrypy': ['cherrypy<19'],
        'gunicorn': ['gunicorn<20'],
        'waitress': ['waitress<1.4'],
        },
    url='https://www.finitelycomputable.net/',
    **base_setup
)
