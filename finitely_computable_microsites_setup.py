version = '19.10.1'
#version += 'a0'

base_setup = {
    'package_dir': {'': '.'},
    'package_data': {'': ['templates/*/*']},
    'data_files': [('', ['README.rst', 'LICENSE.txt'])],
    'include_package_data': False,
    'license': 'AGPL-3.0-only',
    'python_requires': '>=3.5',
    'author': 'Samuel Newbold',
    'author_email': 'sam@rwsh.org',
    'classifiers': [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
}
