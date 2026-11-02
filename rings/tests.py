from datetime import date, timedelta
from decimal import Decimal
from unittest import mock

import cloudinary.exceptions
from django.contrib.auth.models import AnonymousUser, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import dateformat, timezone

from .forms import STONE_STYLES, RingForm
from .models import Favourite, Ring


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


class HomePageTests(TestCase):
    """The home page, from the See the newest rings story."""

    def setUp(self):
        self.owner = User.objects.create_user("amy", password="Test-pass-123")

    def test_home_page_shows_the_three_newest_rings(self):
        now = timezone.now()
        names = ["Newest", "Second", "Third", "Oldest"]
        for days_old, name in enumerate(names):
            ring = make_ring(self.owner, name=name)
            Ring.objects.filter(pk=ring.pk).update(
                created_on=now - timedelta(days=days_old)
            )
        response = self.client.get(reverse("home"))
        shown = [ring.name for ring in response.context["latest_rings"]]
        self.assertEqual(shown, ["Newest", "Second", "Third"])
        self.assertNotContains(response, "Oldest")

    def test_message_shows_when_there_are_no_rings_yet(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "No rings yet")

    def test_see_all_rings_opens_the_all_rings_page(self):
        link = f'href="{reverse("ring_list")}">See all rings'
        self.assertContains(self.client.get(reverse("home")), link)

    def test_newest_rings_link_to_their_own_pages(self):
        ring = make_ring(self.owner, name="Aurora")
        response = self.client.get(reverse("home"))
        self.assertContains(response, f'href="{ring.get_absolute_url()}"')

    @mock.patch("rings.views.timezone.localdate")
    def test_christmas_snow_shows_in_the_season(self, mock_localdate):
        for day in [date(2026, 11, 1), date(2026, 12, 25), date(2027, 1, 6)]:
            with self.subTest(day=day):
                mock_localdate.return_value = day
                response = self.client.get(reverse("home"))
                self.assertContains(response, "christmas season-effect")
                self.assertContains(response, "Pause the snow")

    @mock.patch("rings.views.timezone.localdate")
    def test_christmas_snow_is_hidden_outside_the_season(self, mock_localdate):
        for day in [date(2026, 10, 31), date(2027, 1, 7)]:
            with self.subTest(day=day):
                mock_localdate.return_value = day
                response = self.client.get(reverse("home"))
                self.assertNotContains(response, "christmas season-effect")
                self.assertNotContains(response, "Pause the snow")


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

    def test_a_ring_called_favourites_gets_its_own_slug(self):
        ring = make_ring(self.owner, name="Favourites")
        self.assertEqual(ring.slug, "favourites-ring")

    def test_rings_and_favourites_have_clear_names_in_the_admin(self):
        ring = make_ring(self.owner, name="Aurora")
        favourite = Favourite.objects.create(user=self.owner, ring=ring)
        self.assertEqual(str(ring), "Aurora")
        self.assertEqual(str(favourite), "Aurora saved by amy")


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


class RingEditTests(TestCase):
    """The Edit ring page, from the Edit my ring story."""

    def setUp(self):
        self.owner = User.objects.create_user("amy", password="Test-pass-123")
        self.other = User.objects.create_user("ben", password="Test-pass-123")
        self.staff = User.objects.create_user(
            "sam", password="Test-pass-123", is_staff=True
        )
        self.ring = make_ring(
            self.owner, name="Aurora", gemstone=Ring.Gemstone.DIAMOND
        )
        self.url = reverse("ring_edit", args=[self.ring.slug])
        self.edit_link = f'href="{self.url}"'

    def test_only_the_owner_and_staff_can_change_a_ring(self):
        self.assertTrue(self.ring.can_be_changed_by(self.owner))
        self.assertTrue(self.ring.can_be_changed_by(self.staff))
        self.assertFalse(self.ring.can_be_changed_by(self.other))
        self.assertFalse(self.ring.can_be_changed_by(AnonymousUser()))

    def test_visitors_and_other_users_do_not_see_edit(self):
        ring_page = self.ring.get_absolute_url()
        self.assertNotContains(self.client.get(ring_page), self.edit_link)
        self.client.force_login(self.other)
        self.assertNotContains(self.client.get(ring_page), self.edit_link)

    def test_the_owner_and_staff_see_edit(self):
        ring_page = self.ring.get_absolute_url()
        self.client.force_login(self.owner)
        self.assertContains(self.client.get(ring_page), self.edit_link)
        self.client.force_login(self.staff)
        self.assertContains(self.client.get(ring_page), self.edit_link)

    def test_visitors_are_sent_to_log_in(self):
        response = self.client.get(self.url)
        login_url = reverse("account_login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")

    def test_mistakes_on_the_edit_form_are_explained(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, form_details(price="0"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please check the form for errors.")
        self.ring.refresh_from_db()
        self.assertEqual(self.ring.price, Decimal("1250.00"))

    def test_other_users_cannot_edit(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        response = self.client.post(self.url, form_details(name="Taken"))
        self.assertEqual(response.status_code, 403)
        self.ring.refresh_from_db()
        self.assertEqual(self.ring.name, "Aurora")

    def test_form_shows_the_current_details(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "rings/ring_form.html")
        self.assertEqual(response.context["form"].instance, self.ring)
        self.assertContains(response, 'value="Aurora"')
        self.assertContains(response, "Save changes")

    def test_owner_saves_changes_and_sees_a_message(self):
        self.client.force_login(self.owner)
        details = form_details(name="Aurora Classic", price="1400")
        response = self.client.post(self.url, details, follow=True)
        self.ring.refresh_from_db()
        self.assertEqual(self.ring.name, "Aurora Classic")
        self.assertEqual(self.ring.price, Decimal("1400"))
        self.assertRedirects(response, self.ring.get_absolute_url())
        self.assertContains(response, "Aurora Classic has been updated.")

    def test_staff_can_edit_any_ring(self):
        self.client.force_login(self.staff)
        self.client.post(self.url, form_details(price="999"))
        self.ring.refresh_from_db()
        self.assertEqual(self.ring.price, Decimal("999"))

    def test_leaving_the_photo_empty_keeps_the_old_one(self):
        self.ring.image = "old-photo"
        self.ring.save()
        self.client.force_login(self.owner)
        self.client.post(self.url, form_details(price="1300"))
        self.ring.refresh_from_db()
        self.assertEqual(self.ring.price, Decimal("1300"))
        self.assertIn("old-photo", self.ring.photo_url)

    @mock.patch("cloudinary.uploader.upload", return_value=FAKE_UPLOAD)
    def test_a_new_photo_replaces_the_old_one(self, upload):
        self.ring.image = "old-photo"
        self.ring.save()
        self.client.force_login(self.owner)
        self.client.post(self.url, form_details(image=photo_file()))
        self.ring.refresh_from_db()
        self.assertIn("test-photo", self.ring.photo_url)


class MyRingsTests(TestCase):
    """The My rings page, from the See my rings story."""

    def setUp(self):
        self.owner = User.objects.create_user("amy", password="Test-pass-123")
        self.other = User.objects.create_user("ben", password="Test-pass-123")
        self.url = reverse("my_rings")

    def test_visitors_are_sent_to_log_in(self):
        response = self.client.get(self.url)
        login_url = reverse("account_login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")

    def test_only_signed_in_users_see_my_rings_in_the_navbar(self):
        link = f'href="{self.url}"'
        self.assertNotContains(self.client.get(reverse("home")), link)
        self.client.force_login(self.owner)
        self.assertContains(self.client.get(reverse("home")), link)

    def test_lists_only_my_rings_with_edit_and_delete(self):
        mine = make_ring(self.owner, name="Aurora")
        make_ring(self.other, name="Borealis")
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertContains(response, "Aurora")
        self.assertNotContains(response, "Borealis")
        self.assertContains(response, reverse("ring_edit", args=[mine.slug]))
        self.assertContains(response, reverse("ring_delete", args=[mine.slug]))

    def test_message_and_add_button_show_when_i_have_no_rings(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertContains(response, "You haven't added any rings yet.")
        self.assertContains(response, "Add your first ring")


class RingDeleteTests(TestCase):
    """Deleting a ring, from the Delete my ring story."""

    def setUp(self):
        self.owner = User.objects.create_user("amy", password="Test-pass-123")
        self.other = User.objects.create_user("ben", password="Test-pass-123")
        self.staff = User.objects.create_user(
            "sam", password="Test-pass-123", is_staff=True
        )
        self.ring = make_ring(self.owner, name="Aurora")
        self.url = reverse("ring_delete", args=[self.ring.slug])

    def test_visitors_and_other_users_do_not_see_delete(self):
        ring_page = self.ring.get_absolute_url()
        self.assertNotContains(self.client.get(ring_page), self.url)
        self.client.force_login(self.other)
        self.assertNotContains(self.client.get(ring_page), self.url)

    def test_the_owner_and_staff_see_delete(self):
        ring_page = self.ring.get_absolute_url()
        self.client.force_login(self.owner)
        self.assertContains(self.client.get(ring_page), self.url)
        self.client.force_login(self.staff)
        self.assertContains(self.client.get(ring_page), self.url)

    def test_opening_the_address_asks_first_and_deletes_nothing(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "rings/ring_confirm_delete.html")
        self.assertContains(response, "Delete Aurora?")
        self.assertTrue(Ring.objects.filter(pk=self.ring.pk).exists())

    def test_visitors_are_sent_to_log_in(self):
        response = self.client.post(self.url)
        login_url = reverse("account_login")
        self.assertRedirects(response, f"{login_url}?next={self.url}")
        self.assertTrue(Ring.objects.filter(pk=self.ring.pk).exists())

    def test_other_users_cannot_delete(self):
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.assertEqual(self.client.post(self.url).status_code, 403)
        self.assertTrue(Ring.objects.filter(pk=self.ring.pk).exists())

    def test_owner_deletes_and_goes_to_my_rings_with_a_message(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.url, follow=True)
        self.assertFalse(Ring.objects.filter(pk=self.ring.pk).exists())
        self.assertRedirects(response, reverse("my_rings"))
        self.assertContains(response, "Aurora has been deleted.")

    def test_staff_can_delete_any_ring(self):
        self.client.force_login(self.staff)
        response = self.client.post(self.url)
        self.assertFalse(Ring.objects.filter(pk=self.ring.pk).exists())
        self.assertRedirects(response, reverse("ring_list"))


class RingSafetyTests(TestCase):
    """Nobody else can change my rings: the Keep my rings safe story."""

    def setUp(self):
        self.owner = User.objects.create_user("amy", password="Test-pass-123")
        self.other = User.objects.create_user("ben", password="Test-pass-123")
        self.ring = make_ring(self.owner, name="Aurora")
        self.edit_url = reverse("ring_edit", args=[self.ring.slug])
        self.delete_url = reverse("ring_delete", args=[self.ring.slug])

    def assert_ring_unchanged(self):
        """The ring still exists, with its old name."""
        self.ring.refresh_from_db()
        self.assertEqual(self.ring.name, "Aurora")

    def test_other_users_see_no_edit_or_delete_buttons(self):
        self.client.force_login(self.other)
        response = self.client.get(self.ring.get_absolute_url())
        self.assertNotContains(response, self.edit_url)
        self.assertNotContains(response, self.delete_url)

    def test_other_users_who_type_the_address_see_the_403_page(self):
        self.client.force_login(self.other)
        for url in [self.edit_url, self.delete_url]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertTemplateUsed(response, "403.html")
                self.assertContains(
                    response, "You can't do that", status_code=403
                )
                response = self.client.post(url, form_details(name="Taken"))
                self.assertEqual(response.status_code, 403)
                self.assert_ring_unchanged()

    def test_visitors_are_sent_to_log_in(self):
        login_url = reverse("account_login")
        for url in [self.edit_url, self.delete_url]:
            with self.subTest(url=url):
                expected = f"{login_url}?next={url}"
                self.assertRedirects(self.client.get(url), expected)
                response = self.client.post(url, form_details(name="Taken"))
                self.assertRedirects(response, expected)
                self.assert_ring_unchanged()


class SiteOwnerTests(TestCase):
    """Managing every ring as the site owner (staff)."""

    def setUp(self):
        self.user = User.objects.create_user("amy", password="Test-pass-123")
        self.staff = User.objects.create_superuser(
            "sam", password="Test-pass-123"
        )
        make_ring(self.user, name="Aurora")
        make_ring(self.user, name="Borealis", style=Ring.Style.BAND)

    def test_staff_see_edit_and_delete_on_every_ring(self):
        self.client.force_login(self.staff)
        for ring in Ring.objects.all():
            with self.subTest(ring=ring.name):
                response = self.client.get(ring.get_absolute_url())
                edit_url = reverse("ring_edit", args=[ring.slug])
                delete_url = reverse("ring_delete", args=[ring.slug])
                self.assertContains(response, edit_url)
                self.assertContains(response, delete_url)

    def test_only_staff_see_the_admin_link(self):
        admin_link = f'href="{reverse("admin:index")}"'
        self.client.force_login(self.user)
        self.assertNotContains(self.client.get(reverse("home")), admin_link)
        self.client.force_login(self.staff)
        self.assertContains(self.client.get(reverse("home")), admin_link)

    def test_admin_lists_rings_with_filters_and_a_search(self):
        self.client.force_login(self.staff)
        url = reverse("admin:rings_ring_changelist")
        response = self.client.get(url)
        self.assertContains(response, "Aurora")
        self.assertContains(response, "Borealis")
        self.assertContains(response, "By style")
        self.assertContains(response, 'id="searchbar"')

        searched = self.client.get(url, {"q": "Borealis"})
        self.assertContains(searched, "Borealis")
        self.assertNotContains(searched, "Aurora")

        filtered = self.client.get(url, {"style__exact": "band"})
        self.assertContains(filtered, "Borealis")
        self.assertNotContains(filtered, "Aurora")


class AnyDeviceTests(TestCase):
    """The parts of the Use it on any device story that code can check."""

    def test_pages_scale_to_the_screen(self):
        response = self.client.get(reverse("home"))
        self.assertContains(
            response, 'content="width=device-width, initial-scale=1"'
        )

    def test_the_navbar_folds_into_a_menu(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "navbar-expand-lg")
        self.assertContains(response, 'class="navbar-toggler"')

    def test_price_box_opens_the_number_keypad_on_phones(self):
        self.assertIn('inputmode="decimal"', str(RingForm()["price"]))


class StyleFilterTests(TestCase):
    """The Style menu on All rings, from the Filter by style story."""

    def setUp(self):
        owner = User.objects.create_user("amy", password="Test-pass-123")
        make_ring(owner, name="Aurora", style=Ring.Style.HALO)
        make_ring(owner, name="Borealis", style=Ring.Style.BAND)
        self.url = reverse("ring_list")

    def names_shown(self, response):
        return sorted(ring.name for ring in response.context["rings"])

    def test_all_rings_has_a_style_menu(self):
        response = self.client.get(self.url)
        self.assertContains(response, '<select class="form-select" id="style"')
        self.assertContains(response, "All styles")
        for value in Ring.Style.values:
            self.assertContains(response, f'<option value="{value}"')

    def test_choosing_a_style_shows_only_that_style(self):
        response = self.client.get(self.url, {"style": "halo"})
        self.assertEqual(self.names_shown(response), ["Aurora"])
        self.assertContains(response, "1 ring in the halo style")

    def test_the_count_shows_every_ring_without_a_style(self):
        response = self.client.get(self.url)
        self.assertEqual(self.names_shown(response), ["Aurora", "Borealis"])
        self.assertContains(response, "2 rings")

    def test_message_and_show_all_rings_when_none_match(self):
        response = self.client.get(self.url, {"style": "trilogy"})
        self.assertContains(response, "No trilogy rings yet.")
        self.assertContains(response, f'href="{self.url}">Show all rings')

    def test_a_style_that_does_not_exist_shows_every_ring(self):
        response = self.client.get(self.url, {"style": "banana"})
        self.assertEqual(self.names_shown(response), ["Aurora", "Borealis"])

    def test_page_links_keep_the_style(self):
        owner = User.objects.get(username="amy")
        for number in range(1, 11):
            make_ring(owner, name=f"Halo {number}", style=Ring.Style.HALO)
        response = self.client.get(self.url, {"style": "halo"})
        link = 'href="?style=halo&amp;sort=newest&amp;page=2"'
        self.assertContains(response, link)


class SortTests(TestCase):
    """The Sort menu on All rings, from the Sort by price story."""

    def setUp(self):
        self.owner = User.objects.create_user("amy", password="Test-pass-123")
        self.url = reverse("ring_list")
        now = timezone.now()
        # Made 0, 1 and 2 days ago, so the newest is "Middle".
        rings = [("Middle", "500"), ("Cheapest", "100"), ("Dearest", "900")]
        for days_old, (name, price) in enumerate(rings):
            ring = make_ring(self.owner, name=name, price=Decimal(price))
            Ring.objects.filter(pk=ring.pk).update(
                created_on=now - timedelta(days=days_old)
            )

    def names_in_order(self, **choices):
        response = self.client.get(self.url, choices)
        return [ring.name for ring in response.context["rings"]]

    def test_the_sort_menu_has_three_choices(self):
        response = self.client.get(self.url)
        for value in ["newest", "price_low", "price_high"]:
            self.assertContains(response, f'<option value="{value}"')

    def test_newest_first_is_the_default(self):
        self.assertEqual(
            self.names_in_order(), ["Middle", "Cheapest", "Dearest"]
        )

    def test_price_low_to_high(self):
        self.assertEqual(
            self.names_in_order(sort="price_low"),
            ["Cheapest", "Middle", "Dearest"],
        )

    def test_price_high_to_low(self):
        self.assertEqual(
            self.names_in_order(sort="price_high"),
            ["Dearest", "Middle", "Cheapest"],
        )

    def test_unknown_values_in_the_address_are_ignored(self):
        self.assertEqual(
            self.names_in_order(style="banana", sort="banana"),
            ["Middle", "Cheapest", "Dearest"],
        )

    def test_the_filter_and_sort_stay_when_i_change_page(self):
        for number in range(1, 11):
            make_ring(self.owner, name=f"Halo {number}",
                      style=Ring.Style.HALO, price=Decimal(number))
        choices = {"style": "halo", "sort": "price_high"}
        first_page = self.client.get(self.url, choices)
        link = 'href="?style=halo&amp;sort=price_high&amp;page=2"'
        self.assertContains(first_page, link)
        second_page = self.client.get(self.url, {**choices, "page": 2})
        self.assertContains(second_page, "selected>Price: high to low")
        names = [ring.name for ring in second_page.context["rings"]]
        self.assertEqual(names, ["Halo 1"])


class SearchTests(TestCase):
    """The search box on All rings, from the Search by name story."""

    def setUp(self):
        owner = User.objects.create_user("amy", password="Test-pass-123")
        make_ring(owner, name="Aurora", style=Ring.Style.HALO)
        make_ring(owner, name="Aurora Borealis", style=Ring.Style.BAND)
        make_ring(owner, name="Evening Star", style=Ring.Style.HALO)
        self.url = reverse("ring_list")

    def names_shown(self, response):
        return sorted(ring.name for ring in response.context["rings"])

    def test_all_rings_has_a_search_box(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'for="q">Search by name</label>')
        self.assertContains(response, 'type="search" id="q" name="q"')

    def test_search_finds_part_of_a_name_in_any_case(self):
        response = self.client.get(self.url, {"q": "AURORA"})
        self.assertEqual(
            self.names_shown(response), ["Aurora", "Aurora Borealis"]
        )
        self.assertContains(response, '2 rings matching "AURORA"')

    def test_search_and_style_work_together(self):
        response = self.client.get(self.url, {"q": "aurora", "style": "halo"})
        self.assertEqual(self.names_shown(response), ["Aurora"])
        self.assertContains(
            response, '1 ring in the halo style matching "aurora"'
        )

    def test_message_and_show_all_rings_when_nothing_matches(self):
        response = self.client.get(self.url, {"q": "zircon"})
        self.assertEqual(self.names_shown(response), [])
        self.assertContains(response, 'No rings match "zircon".')
        self.assertContains(response, f'href="{self.url}">Show all rings')

    def test_spaces_alone_show_every_ring(self):
        response = self.client.get(self.url, {"q": "   "})
        self.assertEqual(len(response.context["rings"]), 3)
        self.assertNotContains(response, "matching")

    def test_the_search_stays_in_the_box_and_the_page_links(self):
        owner = User.objects.get(username="amy")
        for number in range(1, 11):
            make_ring(owner, name=f"Star {number}")
        response = self.client.get(self.url, {"q": "star"})
        self.assertContains(response, 'value="star"')
        link = 'href="?style=&amp;sort=newest&amp;q=star&amp;page=2"'
        self.assertContains(response, link)

    def test_a_search_is_shown_as_text_not_run_as_code(self):
        response = self.client.get(self.url, {"q": "<b>Aurora</b>"})
        self.assertContains(response, "&lt;b&gt;Aurora&lt;/b&gt;")
        self.assertNotContains(response, "<b>Aurora</b>")


class FavouriteTests(TestCase):
    """Saving rings, from the Save favourite rings story."""

    def setUp(self):
        self.owner = User.objects.create_user("amy", password="Test-pass-123")
        self.other = User.objects.create_user("ben", password="Test-pass-123")
        self.ring = make_ring(self.owner, name="Aurora")
        self.save_url = reverse("toggle_favourite", args=[self.ring.slug])
        self.url = reverse("favourites")

    def test_visitors_are_sent_to_log_in(self):
        login_url = reverse("account_login")
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{login_url}?next={self.url}")
        response = self.client.post(self.save_url)
        self.assertRedirects(response, f"{login_url}?next={self.save_url}")
        self.assertFalse(Favourite.objects.exists())

    def test_visitors_see_a_log_in_link_instead_of_the_button(self):
        response = self.client.get(self.ring.get_absolute_url())
        self.assertContains(response, "to save this ring to your favourites")
        self.assertNotContains(response, "Save to favourites")

    def test_only_signed_in_users_see_favourites_in_the_navbar(self):
        link = f'href="{self.url}"'
        self.assertNotContains(self.client.get(reverse("home")), link)
        self.client.force_login(self.other)
        self.assertContains(self.client.get(reverse("home")), link)

    def test_saving_a_ring_adds_it_with_a_message(self):
        self.client.force_login(self.other)
        response = self.client.post(self.save_url, follow=True)
        self.assertRedirects(response, self.ring.get_absolute_url())
        self.assertTrue(
            Favourite.objects.filter(user=self.other, ring=self.ring).exists()
        )
        self.assertContains(
            response, "Aurora has been saved to your favourites."
        )
        self.assertContains(response, "Remove from favourites")

    def test_pressing_the_button_again_removes_it(self):
        Favourite.objects.create(user=self.other, ring=self.ring)
        self.client.force_login(self.other)
        response = self.client.post(self.save_url, follow=True)
        self.assertFalse(Favourite.objects.exists())
        self.assertContains(
            response, "Aurora has been removed from your favourites."
        )
        self.assertContains(response, "Save to favourites")

    def test_favourites_lists_only_my_saved_rings_newest_first(self):
        borealis = make_ring(self.owner, name="Borealis")
        make_ring(self.owner, name="Corona")
        older = Favourite.objects.create(user=self.other, ring=self.ring)
        Favourite.objects.filter(pk=older.pk).update(
            created_on=timezone.now() - timedelta(days=1)
        )
        Favourite.objects.create(user=self.other, ring=borealis)
        Favourite.objects.create(user=self.owner, ring=self.ring)
        self.client.force_login(self.other)
        response = self.client.get(self.url)
        names = [ring.name for ring in response.context["rings"]]
        self.assertEqual(names, ["Borealis", "Aurora"])
        self.assertNotContains(response, "Corona")

    def test_message_and_browse_button_show_with_no_favourites(self):
        self.client.force_login(self.other)
        response = self.client.get(self.url)
        self.assertContains(response, "You haven't saved any rings yet.")
        self.assertContains(response, f'href="{reverse("ring_list")}"')

    def test_removing_on_the_favourites_page_goes_back_there(self):
        Favourite.objects.create(user=self.other, ring=self.ring)
        self.client.force_login(self.other)
        response = self.client.post(self.save_url, {"next": self.url})
        self.assertRedirects(response, self.url)
        self.assertFalse(Favourite.objects.exists())

    def test_next_address_on_another_website_is_ignored(self):
        self.client.force_login(self.other)
        response = self.client.post(
            self.save_url, {"next": "https://example.com/"}
        )
        self.assertRedirects(response, self.ring.get_absolute_url())

    def test_the_save_address_only_accepts_post(self):
        self.client.force_login(self.other)
        response = self.client.get(self.save_url)
        self.assertEqual(response.status_code, 405)
        self.assertFalse(Favourite.objects.exists())

    def test_a_ring_can_only_be_saved_once_by_each_user(self):
        Favourite.objects.create(user=self.other, ring=self.ring)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Favourite.objects.create(user=self.other, ring=self.ring)

    def test_deleting_a_ring_removes_it_from_favourites(self):
        Favourite.objects.create(user=self.other, ring=self.ring)
        self.ring.delete()
        self.assertFalse(Favourite.objects.exists())


class ErrorPageTests(TestCase):
    """The 404 and 403 pages, from the Helpful error pages story."""

    def setUp(self):
        self.owner = User.objects.create_user("amy", password="Test-pass-123")
        self.other = User.objects.create_user("ben", password="Test-pass-123")
        self.ring = make_ring(self.owner, name="Aurora")

    def test_a_missing_page_shows_the_404_page_with_links_back(self):
        for url in ["/no-such-page/", "/rings/no-such-ring/"]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertTemplateUsed(response, "404.html")
                self.assertContains(
                    response, "We can't find that page", status_code=404
                )
                for name in ["home", "ring_list"]:
                    link = f'href="{reverse(name)}"'
                    self.assertContains(response, link, status_code=404)

    def test_a_forbidden_action_shows_the_403_page(self):
        self.client.force_login(self.other)
        response = self.client.get(
            reverse("ring_edit", args=[self.ring.slug])
        )
        self.assertTemplateUsed(response, "403.html")
        self.assertContains(response, "You can't do that", status_code=403)

    def test_both_pages_match_the_rest_of_the_site(self):
        self.client.force_login(self.other)
        missing = self.client.get("/no-such-page/")
        forbidden = self.client.get(
            reverse("ring_delete", args=[self.ring.slug])
        )
        for response in [missing, forbidden]:
            with self.subTest(status=response.status_code):
                self.assertTemplateUsed(response, "base.html")
                self.assertContains(
                    response, "Signed in as", status_code=response.status_code
                )
