from django.test import Client, TestCase

class DjangoAppsTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_wsgi_info(self):
        resp = self.c.get('/wsgi_info/')
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.content), 75)
        self.assertLess(len(resp.content), 95)

    def test_helloworld_django(self):
        resp = self.c.get('/hello_world/')
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.content), 25)
        self.assertLess(len(resp.content), 30)
