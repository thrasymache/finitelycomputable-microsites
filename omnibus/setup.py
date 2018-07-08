import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
version = '0.3.dev0'

setup(
    name='omnibus',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='AGPL-3.0-only',
    description='All of Sam Newbold\'s microsites together',
    long_description=README,
    install_requires=[
        'Django>=2.0,<2.1',
        'django-choices>=1.6,<1.7',
        'id_trust==' + version],
    url='https://www.example.com/',
    author='Samuel Newbold',
    author_email='sam@rwsh.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
