def run():
    from sys import argv
    from django.core.management import execute_from_command_line

    if len(argv) <= 1:
        argv.append('help')
    elif len(argv) > 1 and argv[1] == 'run':
        argv[1] = 'runserver'
    command_line = (
        argv[0:2] +
        ['--settings', 'finitelycomputable.django_apps.settings.dev'] +
        argv[2:]
    )
    execute_from_command_line(command_line)


def bjoern():
    '''
    For other options in running bjoern see https://github.com/jonashaag/bjoern
    '''
    from finitelycomputable.django_apps.wsgi import application
    import bjoern
    import sys
    try:
        if len(sys.argv) == 2:
            socket_port = int(sys.argv[1])
        else:
            socket_port = 8000
        bjoern.run(application, "0.0.0.0", socket_port)
    except KeyboardInterrupt:
        sys.exit(1)

def cherry():
    from finitelycomputable.django_apps.wsgi import application
    import cherrypy
    from sys import argv

    cherrypy.tree.graft(application, "/")
    cherrypy.server.unsubscribe()
    server = cherrypy._cpserver.Server()
    server.socket_host = "0.0.0.0"
    if len(argv) == 2:
        server.socket_port = int(argv[1])
    else:
        server.socket_port = 8000
    server.thread_pool = 30
    server.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
