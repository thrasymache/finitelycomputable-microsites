================
Flask-Dispatcher
================

This application provides a /wsgi_info/ endpoint and uses
werkzeug.middleware.dispatcher.DispatcherMiddleware() to
combine all of the Flask modules that it finds in the virtual environment. The
end result does not support ``flask routes`` listing routes other than
``wsgi_info``, but it does support implementations of those endpoints in
frameworks other than Flask.
