from django.test import Client, TestCase

from . import models


def default_create():
    models.Interaction.objects.create(
        foil_strategy='C',
        user_miscommunication=0.0,
        foil_miscommunication=0.0,
    )


class IdTrustViews(TestCase):
    def setUp(self):
        self.c = Client()

    def test_home_200(self):
        resp = self.c.get('/identification_of_trust/')
        self.assertEqual(resp.status_code, 200)

    def test_interact_get_404(self):
        resp = self.c.get('/identification_of_trust/interact/1')
        self.assertEqual(resp.status_code, 404)

    def test_interact_get_200(self):
        default_create()
        resp = self.c.get('/identification_of_trust/interact/1')
        self.assertEqual(resp.status_code, 200)

    def test_post_home_creates_interaction(self):
        self.assertEqual(models.Interaction.objects.count(), 0)
        resp = self.c.post('/identification_of_trust/',
                {'user_intent': 'Trust'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(models.Interaction.objects.count(), 1)

    def test_post_trust_creates_exchange(self):
        self.assertEqual(models.Exchange.objects.count(), 0)
        default_create()
        resp = self.c.post('/identification_of_trust/interact/1',
                {'user_intent': 'Trust'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(models.Exchange.objects.count(), 1)

    def test_post_distrust_creates_exchange(self):
        self.assertEqual(models.Exchange.objects.count(), 0)
        default_create()
        resp = self.c.post('/identification_of_trust/interact/1',
                {'user_intent': 'Distrust'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(models.Exchange.objects.count(), 1)

    def test_class_home_get_200(self):
        resp = self.c.get('/identification_of_trust/class_home')
        self.assertEqual(resp.status_code, 200)
