setup-targets ::= cherrypy-mount/setup.py django-apps/setup.py \
	flask-dispatcher/setup.py flask-blueprints/setup.py \
	falcon-addroute/setup.py \
	helloworld-cherrypy/setup.py \
	helloworld-cherrypy-falcon/setup.py helloworld-cherrypy-flask/setup.py \
	helloworld-cherrypy-morepath/setup.py helloworld-django/setup.py \
	helloworld-falcon/setup.py helloworld-falcon-cherrypy/setup.py \
	helloworld-falcon-flask/setup.py helloworld-falcon-morepath/setup.py \
	helloworld-flask/setup.py helloworld-flask-cherrypy/setup.py \
	helloworld-flask-falcon/setup.py helloworld-flask-morepath/setup.py \
	helloworld-morepath/setup.py helloworld-morepath-cherrypy/setup.py \
	helloworld-morepath-falcon/setup.py helloworld-morepath-flask/setup.py \
	idtrust-common/setup.py \
	idtrust-app-flask/setup.py idtrust-flask-peewee/setup.py \
	idtrust-db-peewee/setup.py idtrust-django/setup.py \
	morepath-mount/setup.py \

all: $(setup-targets)
clean:
	rm $(setup-targets)

cherrypy-mount/setup.py: setup/cherrypy setup/wsgi
django-apps/setup.py: setup/django setup/wsgi
falcon-addroute/setup.py: setup/falcon setup/wsgi
flask-dispatcher/setup.py: setup/flask setup/wsgi
flask-blueprints/setup.py: setup/flask setup/wsgi
helloworld-cherrypy-falcon/setup.py: setup/cherrypy setup/falcon setup/wsgi
helloworld-cherrypy/setup.py: setup/cherrypy setup/wsgi
helloworld-cherrypy-flask/setup.py: setup/cherrypy setup/wsgi
helloworld-cherrypy-morepath/setup.py: setup/cherrypy setup/wsgi
helloworld-django/setup.py: setup/django setup/wsgi
helloworld-falcon/setup.py: setup/falcon setup/wsgi
helloworld-falcon-cherrypy/setup.py: setup/falcon setup/wsgi
helloworld-falcon-flask/setup.py: setup/falcon setup/wsgi
helloworld-falcon-morepath/setup.py: setup/falcon setup/wsgi
helloworld-flask/setup.py: setup/flask setup/wsgi
helloworld-flask-cherrypy/setup.py: setup/flask setup/wsgi
helloworld-flask-falcon/setup.py: setup/flask setup/falcon setup/wsgi
helloworld-flask-morepath/setup.py: setup/flask setup/wsgi
helloworld-morepath/setup.py: setup/morepath setup/wsgi
helloworld-morepath-cherrypy/setup.py: setup/morepath setup/wsgi
helloworld-morepath-falcon/setup.py: setup/morepath setup/falcon setup/wsgi
helloworld-morepath-flask/setup.py: setup/morepath setup/wsgi
idtrust-db-peewee/setup.py: setup/peewee
idtrust-django/setup.py: setup/jinja2 setup/django setup/wsgi
idtrust-app-flask/setup.py: setup/flask setup/wsgi
idtrust-flask-peewee/setup.py: setup/flask setup/wsgi
morepath-mount/setup.py: setup/morepath setup/wsgi

setup-gen.awk: setup/preamble setup/invocation
	touch $@

%/setup.py: setup-gen.awk setup/%
	$^ >$@
	chmod a+x $@
