================
Flask-Blueprints
================

This application provides a /wsgi_info/ endpoint and uses register_blueprint() to
combine all of the Flask modules that it finds in the virtual environment. The
end result is that ``flask routes`` will list all routes from all modules.
