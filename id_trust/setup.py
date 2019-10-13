import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
version = '19.10'
#version += '.dev0'

setup(
    name='id_trust',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    license='AGPL-3.0-only',
    description='A microsite to explore identifying game-theory strategies',
    long_description=README,
    install_requires=['Django>2.1,<3.0', 'django-choices>=1.6,<1.7'],
    url='https://www.example.com/id_trust',
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
