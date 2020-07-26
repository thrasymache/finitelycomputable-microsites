from django.test import Client, TestCase

class IdTrustViews(TestCase):
    def setUp(self):
        self.c = Client()

    def test_home(self):
        resp = self.c.get('/identification_of_trust/')
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.content), 485)
        self.assertLess(len(resp.content), 495)

    def test_real_interact(self):
        resp = self.c.get('/identification_of_trust/real/1')
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.content), 485)
        self.assertLess(len(resp.content), 495)

    def test_reveal_interact(self):
        resp = self.c.get('/identification_of_trust/reveal/1')
        self.assertEqual(resp.status_code, 200)
        self.assertGreater(len(resp.content), 580)
        self.assertLess(len(resp.content), 590)
