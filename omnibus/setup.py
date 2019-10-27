import os
from setuptools import find_packages, setup
from finitely_computable_microsites_setup import version, base_setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='omnibus',
    version=version,
    packages=find_packages('.'),
    description='The microsites of finitelycomputable.net run inside Django',
    long_description=README,
    scripts=[
        'manage.py',
        'cherry-server.py',
        'bjoern-server.py',
        'finitely_computable_microsites_setup.py'],
    install_requires=[
        'Django>2.1,<3.0',
        'django-choices~=1.6',
        'cherrypy<19',
        'id_trust==' + version],
    extras_require={
        'bjoern': ['bjoern<4'],
        'gunicorn': ['gunicorn<20'],
        },
    url='https://www.finitelycomputable.net/',
    **base_setup
)
