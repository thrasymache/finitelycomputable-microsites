dist-dirs ::= cherrypy-mount/. django-apps/. flask-dispatcher/. \
	flask-blueprints/. falcon-addroute/. morepath-mount/. \
	finitelycomputable-tests/. \
	helloworld-cherrypy/. helloworld-cherrypy-falcon/. \
	helloworld-cherrypy-flask/. helloworld-cherrypy-morepath/. \
	helloworld-cherrypy-quart/. \
	helloworld-django/. \
	helloworld-falcon/. helloworld-falcon-cherrypy/. \
	helloworld-falcon-flask/. helloworld-falcon-morepath/. \
	helloworld-falcon-quart/. \
	helloworld-flask/. helloworld-flask-cherrypy/. \
	helloworld-flask-falcon/. helloworld-flask-morepath/. \
	helloworld-flask-quart/. \
	helloworld-morepath/. helloworld-morepath-cherrypy/. \
	helloworld-morepath-falcon/. helloworld-morepath-flask/. \
	helloworld-morepath-quart/. \
	helloworld-quart/. helloworld-quart-cherrypy/. \
	helloworld-quart-falcon/. helloworld-quart-flask/. \
	helloworld-quart-morepath/. \
	idtrust-common/. idtrust-app-flask/. idtrust-flask-peewee/. \
	idtrust-app-falcon/. idtrust-falcon-peewee/. \
	idtrust-db-peewee/. idtrust-django/. \

toml-files ::= $(dist-dirs:%/.=%/pyproject.toml)
whl-files ::= $(dist-dirs:%/.=%/latest.whl)
sdist-files ::= $(dist-dirs:%/.=%/latest.tar.gz)
tests-files ::= unguarded_tests/test_idtrust_falcon.py unguarded_tests/test_idtrust_flask.py

check: latest.whl latest.tar.gz
	twine check $(whl-files)
	twine check $(sdist-files)
check-wheel-contents: latest.whl
	check-wheel-contents --ignore W004 `readlink $(whl-files)`
clean:
	rm -r $(toml-files) $(whl-files) $(sdist-files) $(tests-files) */build
pyproject.toml: $(toml-files)
tests: $(tests-files)
latest.tar.gz: $(sdist-files)
latest.whl: $(whl-files)
requirements:
	sed -i s/~=2.\..*/~=`tr -d \\\n <pyproject/version`/ requirements/*.txt
test:
	pytest --pyargs finitelycomputable.tests.tests_with_import_guards

upload: check
	# only upload most recent version when that isn't everything anyway
	twine upload `readlink $(whl-files) $(sdist-files)`

.PHONY: pyproject.toml check clean latest.tar.gz latest.whl requirements \
	$(whl-files:%/latest.whl=%/check) test tests upload

cherrypy-mount/pyproject.toml: pyproject/cherrypy pyproject/wsgi
django-apps/pyproject.toml: pyproject/django pyproject/wsgi
falcon-addroute/pyproject.toml: pyproject/falcon pyproject/wsgi
flask-dispatcher/pyproject.toml: pyproject/flask pyproject/wsgi
flask-blueprints/pyproject.toml: pyproject/flask pyproject/wsgi
helloworld-cherrypy-falcon/pyproject.toml: pyproject/cherrypy pyproject/falcon pyproject/wsgi
helloworld-cherrypy/pyproject.toml: pyproject/cherrypy pyproject/wsgi
helloworld-cherrypy-flask/pyproject.toml: pyproject/cherrypy pyproject/wsgi
helloworld-cherrypy-morepath/pyproject.toml: pyproject/cherrypy pyproject/wsgi
helloworld-cherrypy-quart/pyproject.toml: pyproject/cherrypy pyproject/wsgi
helloworld-django/pyproject.toml: pyproject/django pyproject/wsgi
helloworld-falcon/pyproject.toml: pyproject/falcon pyproject/wsgi
helloworld-falcon-cherrypy/pyproject.toml: pyproject/falcon pyproject/wsgi
helloworld-falcon-flask/pyproject.toml: pyproject/falcon pyproject/wsgi
helloworld-falcon-morepath/pyproject.toml: pyproject/falcon pyproject/wsgi
helloworld-falcon-quart/pyproject.toml: pyproject/falcon pyproject/wsgi
helloworld-flask/pyproject.toml: pyproject/flask pyproject/wsgi
helloworld-flask-cherrypy/pyproject.toml: pyproject/flask pyproject/wsgi
helloworld-flask-falcon/pyproject.toml: pyproject/flask pyproject/falcon pyproject/wsgi
helloworld-flask-morepath/pyproject.toml: pyproject/flask pyproject/wsgi
helloworld-flask-quart/pyproject.toml: pyproject/flask pyproject/wsgi
helloworld-morepath/pyproject.toml: pyproject/morepath pyproject/wsgi
helloworld-morepath-cherrypy/pyproject.toml: pyproject/morepath pyproject/wsgi
helloworld-morepath-falcon/pyproject.toml: pyproject/morepath pyproject/falcon pyproject/wsgi
helloworld-morepath-flask/pyproject.toml: pyproject/morepath pyproject/wsgi
helloworld-morepath-quart/pyproject.toml: pyproject/morepath pyproject/wsgi
helloworld-quart/pyproject.toml: pyproject/quart
helloworld-quart-cherrypy/pyproject.toml: pyproject/quart
helloworld-quart-falcon/pyproject.toml: pyproject/quart
helloworld-quart-flask/pyproject.toml: pyproject/quart
helloworld-quart-morepath/pyproject.toml: pyproject/quart
idtrust-db-peewee/pyproject.toml: pyproject/peewee
idtrust-django/pyproject.toml: pyproject/jinja2 pyproject/django pyproject/wsgi
idtrust-app-falcon/pyproject.toml: pyproject/falcon pyproject/wsgi
idtrust-app-flask/pyproject.toml: pyproject/flask pyproject/wsgi
idtrust-falcon-peewee/pyproject.toml: pyproject/falcon pyproject/wsgi
idtrust-flask-peewee/pyproject.toml: pyproject/flask pyproject/wsgi
morepath-mount/pyproject.toml: pyproject/morepath pyproject/wsgi

pyproject-gen.awk: pyproject/preamble pyproject/all
	touch $@

%/pyproject.toml: pyproject-gen.awk pyproject/%
	awk -f $^ pyproject/all >$@

%/latest.tar.gz: %/pyproject.toml
	python3 -m build $(dir $<)
	ln -sbT dist/`awk -f sdistname.awk $<` $@

%/latest.whl: %/pyproject.toml | %/latest.tar.gz
	ln -sbT dist/`awk -f wheelname.awk $<` $@

%/check: %/latest.whl
	check-wheel-contents --ignore W004 `readlink $<`
	twine check `readlink $<`

unguarded_tests/test_%_falcon.py: fragments_of_tests/head_%_falcon.py fragments_of_tests/tail_%.py
	cat $^ >$@
unguarded_tests/test_%_flask.py: fragments_of_tests/head_%_flask.py fragments_of_tests/tail_%.py
	cat $^ >$@
