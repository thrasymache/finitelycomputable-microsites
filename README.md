## Environment Variables
The following environment variables are utilized by these microsites:

### DJANGO\_SECRET\_KEY
Django will not run without this value.  This is generated for you in
`django-admin startproject`, but to serve its purpose it needs to remain
secret, so you can't host a publically accessible site and leave this value in
publically accessible version control before. So I took the same approach as
djangopackages.org (https://github.com/djangopackages/djangopackages) and made
it an environment variable after rotating the original key, before publishing
the repo which had the original key in its history. You can use the same
function that Django uses by running in a python shell
`from django.core.management.utils import get_random_secret_key`
`get_random_secret_key()`
or, you can use a password manager or some other password generator.

### DJANGO\_SETTINGS\_MODULE
Django will not run without this value. Use
`DJANGO_SETTINGS_MODULE=finitelycomputable.django_apps.settings.dev` to develop
locally.  To deploy publically you will need to (at a minimum) list your
hostname in ALLOWED\_HOSTS and set the SECURE\* settings based upon whether it
will be served using SSL.

### BASE\_PATH
This value gives the root url of the identification of trust microsite. If it
is not set then it defaults to `identification_of_trust/`. you can use
`BASE_PATH= ` to run it without any path prefixed, and you can run two
separate servers on the same host (likely running different versions or
different configurations) by giving each a different values for this
environemnt variable.

### MICROSITES\_VERSION\_PATH and MICROSITES\_VERSION\_TEXT
In developing software there is a recurrent problem of making some change to
the implementation and needing to validate that that change did not modify the
behavior, but if it does not modify the behavior, then it is hard to be certain
that the changed implementation was actually what you were testing. This lets
you specify some additional information at runtime to help in these sorts of
situations. It also lets you display which version and configuration is
running, if you so choose.

**Installing base packages**
Install finitelycomputable-django-apps and finitelycomputable-idtrust-django
into a virtual environment.  This installs the whole Django Project into the
virtual environment, and as a result the following commands can be run from
anywhere.

To create an empty database when first running the site or when
starting a server in a new directory, run `manage.py migrate`. (Since
the SQLite database is placed in the working directory, you can have
multiple installations with distinct databases using a single virtual
environment and different working directories.)

**Installing extras and running servers**
The following pip install arguments permit you to run an HTTP server on port
9000 with the corresponding commands:

- finitelycomputable-django-apps: `finitelycomputable-django-apps runserver 9000` (Django dev server)
- finitelycomputable-django-apps[cherrypy] : `finitelycomputable-django-apps-cherry 9000` (cheroot using CherryPy)
(note that cheroot is a dependency of cherrypy, so the above pip install also
permits the below usage)
- finitelycomputable-django-apps[cheroot] : `cheroot --bind 0.0.0.0:9000 finitelycomputable.django\_apps.wsgi` (cheroot alone)
- finitelycomputable-django-apps[gunicorn] : `gunicorn -b 0.0.0.0:9000 finitelycomputable.django\_apps.wsgi
- finitelycomputable-django-apps[bjoern] : `finitelycomputable-django-apps-bjoern 9000`
- finitelycomputable-django-apps[waitress] : waitress-serve --port=9000 finitelycomputable.django\_apps.wsgi:application


finitelycomputable-django-apps-cherry and finitelycomputable-django-apps-bjoern
are scripts that are part of the the finitelycomputable-django-apps package
because cherrypy and bjoern take their configuration as arguments in a Python
function call, while the cheroot and gunicorn packages each provide a short
executable script of the same name to pass arguments on the command line.
(For example you can run `cat $(which gunicorn)` to view the one for gunicorn.

## Packaging
individual packages have symlinks to a project-wide dist directory that is not
part of the repo, this enables you to have working copies / worktrees that
cannot be used to make distributions (e.g. to ensure that all needed files are
version-controlled).

1. You will want to install the distribution requirements in a virtualenv:
   `pip install -U -r requirements/dist.txt`
2.  `make latest.whl latest.tar.gz`
   this will build any setup.py files whose components have changed, then build
   the bdist_wheel and sdist packages of those, and make symlinks latest.tar.gz
   and latest.whl respectively to them.
4. `make check-wheel-contents`
5. `make check`
6. `make upload` -- you will need to have your own PyPi account for
   this and to have given the packages a unique name, or the upload will be
   rejected for you not having write permission for the finitelycomputabe-*
   packages.

Note, that the check-wheel-contents target just uses the check-wheel-contents
script and passes to it all of the latest built packages, and that the check
and upload targets just pass the latest built packages to twine check and twine
upload respectively.
