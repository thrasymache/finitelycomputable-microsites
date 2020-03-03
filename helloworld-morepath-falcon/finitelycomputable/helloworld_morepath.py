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
    return resp.body


if environ.get('BASE_PATH'):
    @CoreApp.mount(path=environ.get('BASE_PATH'), app=HelloWorldApp)
    def mount_hello_world():
        return HelloWorldApp()
    application = CoreApp()
else:
    application = HelloWorldApp()


def run():
    from sys import argv
    if len(argv)== 2:
        morepath.run(application, port=(argv[1]))
    else:
        morepath.run(application, port=8080)
