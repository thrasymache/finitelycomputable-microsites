setup-files ::= cherrypy-mount/setup.py django-apps/setup.py \
	flask-dispatcher/setup.py flask-blueprints/setup.py \
	falcon-addroute/setup.py \
	helloworld-cherrypy/setup.py \
	helloworld-cherrypy-falcon/setup.py helloworld-cherrypy-flask/setup.py \
	helloworld-cherrypy-morepath/setup.py helloworld-cherrypy-quart/setup.py \
	helloworld-django/setup.py \
	helloworld-falcon/setup.py helloworld-falcon-cherrypy/setup.py \
	helloworld-falcon-flask/setup.py helloworld-falcon-morepath/setup.py \
	helloworld-flask/setup.py helloworld-flask-cherrypy/setup.py \
	helloworld-flask-falcon/setup.py helloworld-flask-morepath/setup.py \
	helloworld-flask-quart/setup.py helloworld-falcon-quart/setup.py \
	helloworld-morepath/setup.py helloworld-morepath-cherrypy/setup.py \
	helloworld-morepath-falcon/setup.py helloworld-morepath-flask/setup.py \
	helloworld-morepath-quart/setup.py \
	helloworld-quart/setup.py helloworld-quart-cherrypy/setup.py \
	helloworld-quart-falcon/setup.py helloworld-quart-flask/setup.py \
	helloworld-quart-morepath/setup.py \
	idtrust-common/setup.py \
	idtrust-app-flask/setup.py idtrust-flask-peewee/setup.py \
	idtrust-db-peewee/setup.py idtrust-django/setup.py \
	morepath-mount/setup.py \

check: latest.whl latest.tar.gz
	twine check $(setup-files:%/setup.py=%/latest.whl)
	twine check $(setup-files:%/setup.py=%/latest.tar.gz)
check-wheel-contents: latest.whl
	check-wheel-contents `readlink $(setup-files:%/setup.py=%/latest.whl)`
setup-clean: $(setup-files:setup.py=setup-clean)
clean:
	rm -r $(setup-files) $(setup-files:%/setup.py=%/latest.whl) \
		$(setup-files:%/setup.py=%/latest.tar.gz) */build
setup.py: $(setup-files)
latest.tar.gz: $(setup-files:%/setup.py=%/latest.tar.gz)
latest.whl: $(setup-files:%/setup.py=%/latest.whl)
upload: check
	# only upload most recent version when that isn't everything anyway
	twine upload `readlink $(setup-files:%/setup.py=%/latest.whl)` \
		`readlink $(setup-files:%/setup.py=%/latest.tar.gz)`

.PHONY: setup.py check clean setup-clean latest.tar.gz latest.whl \
	$(setup-files:setup.py=setup-clean)
	$(setup-files:setup.py=twine-check)

cherrypy-mount/setup.py: setup/cherrypy setup/wsgi
django-apps/setup.py: setup/django setup/wsgi
falcon-addroute/setup.py: setup/falcon setup/wsgi
flask-dispatcher/setup.py: setup/flask setup/wsgi
flask-blueprints/setup.py: setup/flask setup/wsgi
helloworld-cherrypy-falcon/setup.py: setup/cherrypy setup/falcon setup/wsgi
helloworld-cherrypy/setup.py: setup/cherrypy setup/wsgi
helloworld-cherrypy-flask/setup.py: setup/cherrypy setup/wsgi
helloworld-cherrypy-morepath/setup.py: setup/cherrypy setup/wsgi
helloworld-cherrypy-quart/setup.py: setup/cherrypy setup/wsgi
helloworld-django/setup.py: setup/django setup/wsgi
helloworld-falcon/setup.py: setup/falcon setup/wsgi
helloworld-falcon-cherrypy/setup.py: setup/falcon setup/wsgi
helloworld-falcon-flask/setup.py: setup/falcon setup/wsgi
helloworld-falcon-morepath/setup.py: setup/falcon setup/wsgi
helloworld-falcon-quart/setup.py: setup/falcon setup/wsgi
helloworld-flask/setup.py: setup/flask setup/wsgi
helloworld-flask-cherrypy/setup.py: setup/flask setup/wsgi
helloworld-flask-falcon/setup.py: setup/flask setup/falcon setup/wsgi
helloworld-flask-morepath/setup.py: setup/flask setup/wsgi
helloworld-flask-quart/setup.py: setup/flask setup/wsgi
helloworld-morepath/setup.py: setup/morepath setup/wsgi
helloworld-morepath-cherrypy/setup.py: setup/morepath setup/wsgi
helloworld-morepath-falcon/setup.py: setup/morepath setup/falcon setup/wsgi
helloworld-morepath-flask/setup.py: setup/morepath setup/wsgi
helloworld-morepath-quart/setup.py: setup/morepath setup/wsgi
helloworld-quart/setup.py: setup/quart
helloworld-quart-cherrypy/setup.py: setup/quart setup/wsgi
helloworld-quart-falcon/setup.py: setup/quart setup/wsgi
helloworld-quart-flask/setup.py: setup/quart setup/wsgi
helloworld-quart-morepath/setup.py: setup/quart setup/wsgi
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

%/setup-clean: %/setup.py
	$< clean --all

%/latest.tar.gz: %/setup.py
	$< sdist bdist_wheel
	ln -sbT dist/`$< --fullname`.tar.gz $@

%/latest.whl: %/setup.py | %/latest.tar.gz
	ln -sbT dist/`$< --fullname | sed -e s/-/_/g -e s/_23/-23/`-py3-none-any.whl $@
