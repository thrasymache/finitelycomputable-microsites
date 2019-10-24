Install id-trust and omnibus into a virtual environment. You can work
around them not being in PyPi by building eggs and installing id-trust
first and omnibus second. This installs the whole Django Project into
the virtual environment, and as a result the following commands can be
run from anywhere.

To create an empty database when first running the site or when
starting a server in a new directory, run `manage.py migrate`. (Since
the SQLite database is placed in the working directory, you can have
multiple installations with distinct databases using a single virtual
environment and different working directories.)

To run using CherryPy for wsgi - `cherry-server.py`
To run using gunicorn `gunicorn omnibus.wsgi`
To run using bjoern for wsgi - `bjoern-server.py`

All three wsgi servers together are one eighth the size of django, but
any or all of them can be omitted with the only impact that the
corresponding command can no longer be used to run a server.

DJANGO\_SECRET ********
