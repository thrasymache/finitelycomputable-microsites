import morepath
from os import environ

from finitelycomputable import helloworld_falcon
from falcon import Response

class HelloWorldApp(morepath.App):
    pass

class CoreApp(morepath.App):
    pass


@HelloWorldApp.path(path='/')
class Root(helloworld_falcon.HelloWorld):
    pass


@HelloWorldApp.view(model=Root, name='')
def hello_world(self, request):
    resp = Response()
    self.on_get(request, resp)
    return 'Morepath adapts, ' + resp.text


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
    morepath.run(application, port=port)
