from decimal import Decimal
from unittest import mock

import cloudinary.exceptions
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import dateformat, timezone

from .forms import STONE_STYLES, RingForm
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


class RingDetailTests(TestCase):
    """A ring's own page, from the View a ring story."""

    def setUp(self):
        self.owner = User.objects.create_user("amy", password="Test-pass-123")
        self.ring = make_ring(
            self.owner,
            name="Aurora",
            gemstone=Ring.Gemstone.DIAMOND,
            description="A bright solitaire.\nMade by hand.",
        )
        self.url = self.ring.get_absolute_url()

    def test_address_is_made_from_the_slug(self):
        self.assertEqual(self.url, "/rings/aurora/")

    def test_page_shows_all_the_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "rings/ring_detail.html")
        self.assertContains(response, "Aurora")
        self.assertContains(response, "£1,250")
        self.assertContains(response, "Solitaire")
        self.assertContains(response, "Yellow gold")
        self.assertContains(response, "Diamond")
        self.assertContains(response, "A bright solitaire.<br>Made by hand.")

    def test_page_shows_who_added_the_ring_and_when(self):
        response = self.client.get(self.url)
        added_on = timezone.localtime(self.ring.created_on)
        self.assertContains(response, "amy")
        self.assertContains(response, dateformat.format(added_on, "j F Y"))

    def test_ring_without_a_photo_shows_a_drawing(self):
        response = self.client.get(self.url)
        self.assertContains(response, "images/styles/solitaire.svg")

    def test_ring_with_a_photo_shows_the_photo(self):
        self.ring.image = "sample"
        self.ring.save()
        response = self.client.get(self.url)
        self.assertContains(response, self.ring.photo_url)
        self.assertContains(response, "Aurora, a yellow gold solitaire ring")

    def test_ring_that_does_not_exist_shows_the_404_page(self):
        response = self.client.get("/rings/no-such-ring/")
        self.assertEqual(response.status_code, 404)

    def test_ring_cards_link_to_the_ring_page(self):
        response = self.client.get(reverse("ring_list"))
        self.assertContains(response, f'href="{self.url}"')


# What Cloudinary sends back after an upload. The tests use it instead of
# uploading, so running them never puts photos in your Cloudinary account.
FAKE_UPLOAD = {
    "public_id": "test-photo",
    "version": 1729340000,
    "format": "jpg",
    "type": "upload",
    "resource_type": "image",
}


def form_details(**changes):
    """What someone types into the Add a ring form."""
    details = {
        "name": "Aurora",
        "style": Ring.Style.SOLITAIRE,
        "metal": Ring.Metal.YELLOW_GOLD,
        "gemstone": Ring.Gemstone.DIAMOND,
        "price": "1250.00",
        "description": "A bright solitaire.",
    }
    details.update(changes)
    return details


def photo_file(size=1024):
    """A small file that stands in for a photo."""
    return SimpleUploadedFile("ring.jpg", b"x" * size, "image/jpeg")


class RingFormTests(TestCase):
    """The checks in RingForm, from the Add a ring story."""

    def test_photo_is_optional(self):
        form = RingForm(data=form_details())
        self.assertTrue(form.is_valid())

    def test_rings_built_around_a_stone_need_a_gemstone(self):
        for style in STONE_STYLES:
            with self.subTest(style=style):
                details = form_details(
                    style=style, gemstone=Ring.Gemstone.NONE
                )
                form = RingForm(data=details)
                self.assertFalse(form.is_valid())
                self.assertIn("gemstone", form.errors)

    def test_a_band_can_have_no_gemstone(self):
        details = form_details(
            style=Ring.Style.BAND, gemstone=Ring.Gemstone.NONE
        )
        self.assertTrue(RingForm(data=details).is_valid())

    def test_price_must_be_at_least_one_pound(self):
        form = RingForm(data=form_details(price="0.99"))
        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)
        self.assertTrue(RingForm(data=form_details(price="1")).is_valid())

    def test_photo_over_5_mb_is_refused(self):
        big_photo = photo_file(size=5 * 1024 * 1024 + 1)
        form = RingForm(data=form_details(), files={"image": big_photo})
        self.assertFalse(form.is_valid())
        self.assertIn("image", form.errors)


class RingCreateTests(TestCase):
    """The Add a ring page, from the Add a ring story."""

    def setUp(self):
        self.user = User.objects.create_user("amy", password="Test-pass-123")
        self.url = reverse("ring_create")

    def test_visitors_are_sent_to_log_in(self):
        response = self.client.get(self.url)
        login_url = reverse("account_login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")

    def test_only_signed_in_users_see_add_a_ring(self):
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, f'href="{self.url}"')
        self.client.force_login(self.user)
        response = self.client.get(reverse("home"))
        self.assertContains(response, f'href="{self.url}"')

    def test_signed_in_users_see_the_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "rings/ring_form.html")

    def test_ring_is_added_with_a_drawing_and_a_message(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, form_details(), follow=True)
        ring = Ring.objects.get(name="Aurora")
        self.assertEqual(ring.owner, self.user)
        self.assertEqual(ring.photo_url, "")
        self.assertRedirects(response, ring.get_absolute_url())
        self.assertContains(response, "Aurora has been added.")
        self.assertContains(response, "images/styles/solitaire.svg")

    @mock.patch("cloudinary.uploader.upload", return_value=FAKE_UPLOAD)
    def test_photo_is_uploaded_to_cloudinary(self, upload):
        self.client.force_login(self.user)
        self.client.post(self.url, form_details(image=photo_file()))
        upload.assert_called_once()
        ring = Ring.objects.get(name="Aurora")
        self.assertIn("test-photo", ring.photo_url)

    @mock.patch(
        "cloudinary.uploader.upload",
        side_effect=cloudinary.exceptions.Error("Invalid image file"),
    )
    def test_a_file_cloudinary_cannot_read_shows_an_error(self, upload):
        self.client.force_login(self.user)
        response = self.client.post(
            self.url, form_details(image=photo_file())
        )
        self.assertContains(response, "Please choose a JPG, PNG or WebP")
        self.assertFalse(Ring.objects.exists())

    def test_mistakes_show_an_error_and_add_nothing(self):
        self.client.force_login(self.user)
        details = form_details(gemstone=Ring.Gemstone.NONE)
        response = self.client.post(self.url, details)
        self.assertContains(response, "Please check the form for errors.")
        self.assertContains(response, "Solitaire rings need a gemstone.")
        self.assertFalse(Ring.objects.exists())
