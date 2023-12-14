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

version = '23.12'

name='finitelycomputable-idtrust-django'
description='A Django microsite to explore identifying game-theory strategies'
entry_points={
    'console_scripts': [
        'finitelycomputable-idtrust-django = finitelycomputable.idtrust_django:run']
    }
url='http://www.finitelycomputable.net/identification_of_trust'

install_requires.append('finitelycomputable-idtrust-common~=' + version)
install_requires.append('jinja2~=3.1')  # to avoid cannot import name 'soft_unicode' from 'markupsafe'
install_requires.append('Django~=4.2.6')
classifiers.append('Framework :: Django')
classifiers.append('Framework :: Django :: 4.2')

extras_require.update({
    'bjoern': ['bjoern~=3.0'],
    'cheroot': ['cheroot~=9.0'],
    'cherrypy': ['cherrypy~=18.0'],
    'gunicorn': ['gunicorn~=20.0'],
    'waitress': ['waitress~=2.1'],
    }
)
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
