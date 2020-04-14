#! /usr/bin/env python
import os
from setuptools import setup
from finitelycomputable_microsites_setup import (
        version, base_setup, wsgi_extras_require,
)

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

extras_require=wsgi_extras_require
extras_require.update({
        'helloworld': ['finitelycomputable-helloworld-flask~=' + version],
        })

setup(
    name='finitelycomputable-flask-dispatcher',
    version=version,
    py_modules=['finitelycomputable.flask_dispatcher'],
    entry_points={
        'console_scripts': [
            'finitelycomputable-flask-dispatcher = finitelycomputable.flask_dispatcher:run']
        },
    description='The Flask-based wsgi app using werkzeug.middleware.dispatcher to combine the microsites of finitelycomputable.net',
    long_description=README,
    long_description_content_type="text/x-rst",
    scripts=['finitelycomputable_microsites_setup.py'],
    install_requires=['Flask~=1.1'],
    extras_require=extras_require,
    url='http://www.finitelycomputable.net/wsgi_info',
    **base_setup
)
