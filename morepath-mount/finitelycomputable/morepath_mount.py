import morepath
from os import environ
from platform import python_version
from posixpath import join

from finitelycomputable_microsites_setup import version


base_path = join('/', environ.get('BASE_PATH', ''))
version_text = environ.get('MICROSITES_VERSION_TEXT', '')
included_apps = []

class CoreApp(morepath.App):
    pass

@CoreApp.path(path=base_path)
class Root(object):
    pass

@CoreApp.view(model=Root, name='wsgi_info')
def wsgi_info(self, request):
    return (
f'''{version_text} using {__name__} {version} on Python {python_version()}
at {base_path} with {', '.join(included_apps) or "nothing"}\n'''
    )

try:
    from finitelycomputable.helloworld_morepath import HelloWorldApp
    @CoreApp.mount(path=join(base_path, 'hello_world'), app=HelloWorldApp)
    def mount_hello_world():
        return HelloWorldApp()
    included_apps.append('helloworld_morepath')
except ModuleNotFoundError:
    pass


application = CoreApp()


def run():
    from sys import argv
    if len(argv)== 2:
        morepath.run(application, port=(argv[1]))
    else:
        morepath.run(application, port=8080)
