#! /usr/bin/env python3
# This is a minor edit of the example config on the Digital Ocean tutorial for
# deploying Django with CherryPy.
# https://www.digitalocean.com/community/tutorials/how-to-deploy-python-wsgi-applications-using-a-cherrypy-web-server-behind-nginx
from omnibus.wsgi import application

# Import CherryPy
import cherrypy
from sys import argv

if __name__ == '__main__':

    # Mount the application
    cherrypy.tree.graft(application, "/")

    # Unsubscribe the default server
    cherrypy.server.unsubscribe()

    # Instantiate a new server object
    server = cherrypy._cpserver.Server()

    # Configure the server object
    server.socket_host = "0.0.0.0"
    if len(argv) == 2:
        server.socket_port = int(argv[1])
    else:
        server.socket_port = 8000
    server.thread_pool = 30

    # For SSL Support
    # server.ssl_module            = 'pyopenssl'
    # server.ssl_certificate       = 'ssl/certificate.crt'
    # server.ssl_private_key       = 'ssl/private.key'
    # server.ssl_certificate_chain = 'ssl/bundle.crt'

    # Subscribe this server
    server.subscribe()

    # Example for a 2nd server (same steps as above):
    # Remember to use a different port

    # server2             = cherrypy._cpserver.Server()

    # server2.socket_host = "0.0.0.0"
    # server2.socket_port = 8081
    # server2.thread_pool = 30
    # server2.subscribe()

    # Start the server engine (Option 1 *and* 2)

    cherrypy.engine.start()
    cherrypy.engine.block()
