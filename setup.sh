#! /bin/sh
# setuputils and distutils make an impressive fraud of being able to simply
# configure multiple distributions (which are the smallest
# independently-installable unit) to be built from the same directory, but back
# in the 70s they understood how to do this sort of thing.
python3 idtrust-common/setup.py $*
python3 idtrust-app-flask/setup.py $*
python3 idtrust-db-peewee/setup.py $*
python3 idtrust-flask-peewee/setup.py $*
python3 idtrust-django/setup.py $*
python3 django-apps/setup.py $*
python3 cherrypy-mount/setup.py $*
python3 falcon-addroute/setup.py $*
python3 flask-blueprints/setup.py $*
python3 flask-dispatcher/setup.py $*
python3 helloworld-cherrypy/setup.py $*
python3 helloworld-django/setup.py $*
python3 helloworld-falcon/setup.py $*
python3 helloworld-flask/setup.py $*
python3 helloworld-morepath/setup.py $*
python3 morepath-mount/setup.py $*
