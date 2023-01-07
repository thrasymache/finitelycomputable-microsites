#! /usr/bin/env python
import os
from setuptools import find_namespace_packages, setup
from finitelycomputable_microsites_setup import (
        version, base_setup, wsgi_extras_require, cherrypy_version,
)

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='finitelycomputable-cherrypy-mount',
    version=version,
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': [
            'finitelycomputable-cherrypy-mount = finitelycomputable.cherrypy_mount:run']
        },
    description='The CherryPy-based wsgi app using tree.mount()for the microsites of finitelycomputable.net',
    long_description=README,
    long_description_content_type="text/x-rst",
    scripts=['finitelycomputable_microsites_setup.py'],
    install_requires=[cherrypy_version],
    extras_require=wsgi_extras_require,
    url='http://www.finitelycomputable.net/wsgi_info',
    **base_setup
)
