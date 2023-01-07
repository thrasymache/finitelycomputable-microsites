try:
    import cherrypy.test.helper
    import pytest

    from finitelycomputable import helloworld_cherrypy

    class HelloWorldTest(cherrypy.test.helper.CPWebCase):
        cherrypy.test.helper.CPWebCase.interactive = False

        def setup_server():
            helloworld_cherrypy.setup_server()
        setup_server = staticmethod(setup_server)

        def test_helloworld_cherrypy(self):
            self.getPage('/')
            self.assertStatus('200 OK')
            self.assertGreater(len(self.body), 21)
            self.assertLess(len(self.body), 30)

        @pytest.mark.xfail
        def test_helloworld_cherrypy_exact(self):
            self.getPage('/')
            self.assertStatus('200 OK')
            self.assertBody(b'CherryPy says "hello, world"\n')
except ImportError:
    pass
