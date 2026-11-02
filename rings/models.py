"""The Ring model: one ring in the Radiant Karats collection."""
from decimal import Decimal

from cloudinary import CloudinaryImage
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# The ring pages use the addresses /rings/add/, /rings/mine/ and
# /rings/favourites/, so no ring may use those words as its slug.
RESERVED_SLUGS = {"add", "mine", "favourites"}


class Ring(models.Model):
    """A ring that a user has added to the collection."""

    class Style(models.TextChoices):
        SOLITAIRE = "solitaire", "Solitaire"
        HALO = "halo", "Halo"
        TRILOGY = "trilogy", "Trilogy"
        ETERNITY = "eternity", "Eternity"
        BAND = "band", "Band"

    class Metal(models.TextChoices):
        YELLOW_GOLD = "yellow_gold", "Yellow gold"
        WHITE_GOLD = "white_gold", "White gold"
        ROSE_GOLD = "rose_gold", "Rose gold"
        PLATINUM = "platinum", "Platinum"
        SILVER = "silver", "Sterling silver"

    class Gemstone(models.TextChoices):
        DIAMOND = "diamond", "Diamond"
        LAB_DIAMOND = "lab_diamond", "Lab-grown diamond"
        MOISSANITE = "moissanite", "Moissanite"
        SAPPHIRE = "sapphire", "Sapphire"
        EMERALD = "emerald", "Emerald"
        RUBY = "ruby", "Ruby"
        NONE = "none", "No gemstone"

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rings"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, editable=False)
    style = models.CharField(max_length=20, choices=Style.choices)
    metal = models.CharField(max_length=20, choices=Metal.choices)
    gemstone = models.CharField(
        max_length=20, choices=Gemstone.choices, default=Gemstone.NONE
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("1.00"))],
        help_text="The price in pounds.",
    )
    description = models.TextField()
    image = CloudinaryField("image", default="placeholder")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gt=0), name="ring_price_above_zero"
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Give a new ring a unique slug made from its name."""
        if not self.slug:
            self.slug = self.make_unique_slug()
        super().save(*args, **kwargs)

    def can_be_changed_by(self, user):
        """Only the ring's owner, or the site owner (staff), may change it."""
        if not user.is_authenticated:
            return False
        return user == self.owner or user.is_staff

    def get_absolute_url(self):
        """The address of this ring's own page."""
        return reverse("ring_detail", args=[self.slug])

    def make_unique_slug(self):
        """Slugify the name, then add a number until no ring uses it."""
        base_slug = slugify(self.name) or "ring"
        if base_slug in RESERVED_SLUGS:
            base_slug = f"{base_slug}-ring"
        slug = base_slug
        number = 2
        while Ring.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{number}"
            number += 1
        return slug

    @property
    def photo_url(self):
        """The photo's web address, or "" if no photo has been uploaded.

        f_auto and q_auto tell Cloudinary to send a small, modern image
        format, such as WebP, to browsers that support it.
        """
        if "placeholder" in str(self.image):
            return ""
        return CloudinaryImage(str(self.image)).build_url(
            secure=True, fetch_format="auto", quality="auto"
        )

    @property
    def placeholder_image(self):
        """The drawing to show until a photo is uploaded."""
        return f"images/styles/{self.style}.svg"

    @property
    def alt_text(self):
        """Describes the photo for people who use screen readers."""
        metal = self.get_metal_display().lower()
        style = self.get_style_display().lower()
        return f"{self.name}, a {metal} {style} ring"


class Favourite(models.Model):
    """A ring that a user has saved, to find again on their Favourites."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favourites"
    )
    ring = models.ForeignKey(
        Ring, on_delete=models.CASCADE, related_name="favourites"
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "ring"], name="one_favourite_per_user_and_ring"
            ),
        ]

    def __str__(self):
        return f"{self.ring} saved by {self.user}"
