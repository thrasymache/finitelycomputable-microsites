import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
version = '19.10.2'
#version += '.dev0'

setup(
    name='omnibus',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='AGPL-3.0-only',
    description='All of Sam Newbold\'s microsites together',
    long_description=README,
    scripts=['manage.py', 'cherry-server.py', 'bjoern-server.py'],
    install_requires=[
        'Django>2.1,<3.0',
        'django-choices<1.7,>=1.6',
        'bjoern<4',
        'cherrypy<19',
        'gunicorn<20',
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
