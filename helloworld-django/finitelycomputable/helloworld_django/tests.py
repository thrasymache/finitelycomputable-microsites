from django.test import Client, TestCase

class HelloWorldTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_helloworld_django(self):
        resp = self.c.get('/hello_world/')
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.content), 25)
        self.assertLess(len(resp.content), 30)

    def test_helloworld_django_exact(self):
        resp = self.c.get('/hello_world/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, b'Django says "hello, world"\n')
