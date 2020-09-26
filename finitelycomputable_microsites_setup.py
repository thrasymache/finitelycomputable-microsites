version = '20.9'
#version += 'a1'

base_setup = {
    'package_dir': {'': '.'},
    'package_data': {'': ['templates/*/*']},
    'data_files': [('', ['README.rst', 'LICENSE.txt'])],
    'include_package_data': False,
    'license': 'AGPL-3.0-only',
    'python_requires': '>=3.6',
    'author': 'Samuel Newbold',
    'author_email': 'sam@rwsh.org',
    'classifiers': [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
    ],
    'project_urls': {
        'Documentation': 'https://github.com/thrasymache/microsites',
        'Source': 'https://github.com/thrasymache/microsites',
    },
}

django_classifiers = [
        'Framework :: Django',
        'Framework :: Django :: 3.0',
    ]

django_setup = base_setup.copy()
django_setup['classifiers'] = django_setup['classifiers'].copy()
django_setup['classifiers'].extend(django_classifiers)

wsgi_extras_require={
        'bjoern': ['bjoern<4'],
        'cheroot': ['cheroot<9'],
        'cherrypy': ['cherrypy<19'],
        'gunicorn': ['gunicorn~=20.0'],
        'waitress': ['waitress~=1.4'],
        }
