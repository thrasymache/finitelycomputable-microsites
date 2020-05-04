import morepath
from os import environ


class HelloWorldApp(morepath.App):
    pass

class CoreApp(morepath.App):
    pass


@HelloWorldApp.path(path='/')
class Root(object):
    pass


@HelloWorldApp.view(model=Root, name='')
def hello_world(self, request):
    return 'Morepath says "hello, world"\n'


if environ.get('BASE_PATH'):
    @CoreApp.mount(path=environ.get('BASE_PATH'), app=HelloWorldApp)
    def mount_hello_world():
        return HelloWorldApp()
    application = CoreApp()
else:
    application = HelloWorldApp()


def run():
    from sys import argv, exit, stderr
    if len(argv) < 2 or argv[1] != 'run':
        stderr.write(f'usage: {argv[0]} run [port]\n')
        exit(1)
    try:
        port=int(argv[2])
    except IndexError:
        port=8080
    morepath.run(application, ignore_cli=True, port=port)
