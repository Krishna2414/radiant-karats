from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Ring


def make_ring(owner, name="Aurora", **details):
    """Save a ring for a test. Any detail can be changed, such as style."""
    fields = {
        "style": Ring.Style.SOLITAIRE,
        "metal": Ring.Metal.YELLOW_GOLD,
        "price": Decimal("1250.00"),
        "description": "A ring for testing.",
    }
    fields.update(details)
    return Ring.objects.create(owner=owner, name=name, **fields)


class RingStoreHomeTests(TestCase):
    def test_homepage_shows_ring_storefront(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Radiant Karats")
        self.assertContains(response, "Solstice Solitaire")
        self.assertContains(response, "The Heirloom")
        self.assertContains(response, "Golden Hour Band")
        self.assertNotContains(response, "Helping Hands")


class RingModelTests(TestCase):
    """The slug that each ring gets from its name."""

    def setUp(self):
        self.owner = User.objects.create_user("amy", password="Test-pass-123")

    def test_slug_is_made_from_the_name(self):
        ring = make_ring(self.owner, name="Golden Hour Band")
        self.assertEqual(ring.slug, "golden-hour-band")

    def test_rings_with_the_same_name_get_different_slugs(self):
        first = make_ring(self.owner, name="Aurora")
        second = make_ring(self.owner, name="Aurora")
        self.assertEqual(first.slug, "aurora")
        self.assertEqual(second.slug, "aurora-2")


class RingListTests(TestCase):
    """The All rings page, from the Browse all rings story."""

    def setUp(self):
        self.owner = User.objects.create_user("amy", password="Test-pass-123")
        self.url = reverse("ring_list")

    def test_page_opens_with_its_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "rings/ring_list.html")

    def test_message_shows_when_there_are_no_rings(self):
        response = self.client.get(self.url)
        self.assertContains(response, "No rings yet")

    def test_card_shows_name_style_metal_and_price(self):
        make_ring(self.owner, name="Aurora")
        response = self.client.get(self.url)
        self.assertContains(response, "Aurora")
        self.assertContains(response, "Solitaire")
        self.assertContains(response, "Yellow gold")
        self.assertContains(response, "£1,250")
        self.assertNotContains(response, "No rings yet")

    def test_ring_without_a_photo_shows_a_drawing(self):
        make_ring(self.owner, style=Ring.Style.HALO)
        response = self.client.get(self.url)
        self.assertContains(response, "images/styles/halo.svg")
        self.assertContains(response, "Halo ring drawing")

    def test_nine_rings_a_page_with_next_and_previous(self):
        for number in range(1, 11):
            make_ring(self.owner, name=f"Ring {number}")

        first_page = self.client.get(self.url)
        self.assertEqual(len(first_page.context["rings"]), 9)
        self.assertContains(first_page, "Next")
        self.assertNotContains(first_page, "Previous")

        second_page = self.client.get(self.url, {"page": 2})
        self.assertEqual(len(second_page.context["rings"]), 1)
        self.assertContains(second_page, "Previous")
        self.assertNotContains(second_page, "Next")

    def test_navbar_links_to_all_rings(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'href="/rings/"')
