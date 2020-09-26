from django.test import Client, TestCase

from . import models


class IdTrustViews(TestCase):
    def setUp(self):
        self.c = Client()

    def test_home_200(self):
        resp = self.c.get('/identification_of_trust/')
        self.assertEqual(resp.status_code, 200)

    def test_interact_get_200(self):
        resp = self.c.get('/identification_of_trust/interact/1')
        self.assertEqual(resp.status_code, 200)

    def test_post_trust_creates_exchange(self):
        self.assertEqual(models.Exchange.objects.count(), 0)
        resp = self.c.post('/identification_of_trust/interact/1',
                {'choice': 'Trust'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(models.Exchange.objects.count(), 1)

    def test_class_home_get_200(self):
        resp = self.c.get('/identification_of_trust/class_home')
        self.assertEqual(resp.status_code, 200)
