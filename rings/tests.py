from django.test import TestCase


class RingStoreHomeTests(TestCase):
    def test_homepage_shows_ring_storefront(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Radiant Karats")
        self.assertContains(response, "Solstice Solitaire")
        self.assertContains(response, "The Heirloom")
        self.assertContains(response, "Golden Hour Band")
        self.assertNotContains(response, "Helping Hands")
