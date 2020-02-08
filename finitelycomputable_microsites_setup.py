version = '20.2'
#version += 'a0'

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

django_setup = {
    'classifiers': [
        'Framework :: Django',
        'Framework :: Django :: 2.0',
    ],
}
