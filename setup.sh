#! /bin/sh
# setuputils and distutils make an impressive fraud of being able to simply
# configure multiple distributions (which are the smallest
# independently-installable unit) to be built from the same directory, but back
# in the 70s they understood how to do this sort of thing.
python idtrust-common/setup.py $*
python idtrust-flask/setup.py $*
python idtrust-django/setup.py $*
python django-apps/setup.py $*
python cherrypy-mount/setup.py $*
python falcon-addroute/setup.py $*
python flask-blueprints/setup.py $*
python flask-dispatcher/setup.py $*
python helloworld-cherrypy/setup.py $*
python helloworld-django/setup.py $*
python helloworld-falcon/setup.py $*
python helloworld-flask/setup.py $*
python helloworld-morepath/setup.py $*
python morepath-mount/setup.py $*
