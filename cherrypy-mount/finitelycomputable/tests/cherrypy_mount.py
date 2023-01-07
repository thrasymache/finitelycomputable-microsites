import cherrypy.test.helper
import pytest

from finitelycomputable import cherrypy_mount

class CherrypyMountTest(cherrypy.test.helper.CPWebCase):
    cherrypy.test.helper.CPWebCase.interactive = False

    def setup_server():
        cherrypy_mount.setup_server()
    setup_server = staticmethod(setup_server)

    def test_wsgi_info(self):
        self.getPage('/wsgi_info/')
        self.assertStatus('200 OK')
        self.assertGreater(len(self.body), 105)
        self.assertLess(len(self.body), 125)

    def test_helloworld_cherrypy(self):
        self.getPage('/hello_world/')
        self.assertStatus('200 OK')
        self.assertGreater(len(self.body), 21)
        self.assertLess(len(self.body), 30)
