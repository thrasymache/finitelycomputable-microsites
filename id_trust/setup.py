import os
from setuptools import find_packages, setup
from finitely_computable_microsites_setup import version, base_setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='id_trust',
    version=version,
    packages=find_packages('.'),
    description='A microsite to explore identifying game-theory strategies',
    long_description=README,
    scripts=['finitely_computable_microsites_setup.py'],
    install_requires=[
        'Django>2.1,<3.0',
        'django-choices~=1.6'],
    url='https://www.finitelycomputable.net/identification_of_trust',
    **base_setup
)
