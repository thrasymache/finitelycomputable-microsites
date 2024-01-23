#! /usr/bin/env python
import os
from setuptools import find_namespace_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

classifiers = [
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Affero General Public License v3',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: WSGI',
]
install_requires = []
extras_require = {}

version = '23.13'

name='finitelycomputable-idtrust-db-peewee'
description='Peewee implementation of database layer for the Identification of Trust microsite'
entry_points={
    'console_scripts': []
    }
url='https://www.finitelycomputable.net/identification_of_trust'
#install_requires=[ peewee_version ]
install_requires.append('peewee~=3.15')
setup(
    name=name,
    classifiers=classifiers,
    description=description,
    entry_points=entry_points,
    extras_require=extras_require,
    install_requires=install_requires,
    url=url,
    version=version,
    author='Samuel Newbold',
    author_email='sam@rwsh.org',
    data_files=[('', ['README.rst', 'LICENSE.txt'])],
    include_package_data=False,
    license='AGPL-3.0-only',
    long_description_content_type="text/x-rst",
    long_description=README,
    package_data={'': ['templates/*', 'templates/*/*']},
    package_dir={'': '.'},
    packages=find_namespace_packages(),
    project_urls={
        'Documentation': 'https://github.com/thrasymache/microsites',
        'Source': 'https://github.com/thrasymache/microsites',
    },
    python_requires='>=3.7',
    scripts=[],
)
