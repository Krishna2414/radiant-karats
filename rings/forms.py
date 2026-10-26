"""The form for adding a ring, and the checks it makes."""
import cloudinary.exceptions
from cloudinary.forms import CloudinaryFileField
from django import forms

from .models import Ring

MAX_PHOTO_MB = 5

# These styles are built around a stone, so they need a gemstone.
STONE_STYLES = [
    Ring.Style.SOLITAIRE,
    Ring.Style.HALO,
    Ring.Style.TRILOGY,
    Ring.Style.ETERNITY,
]


class PhotoField(CloudinaryFileField):
    """A photo upload that turns upload problems into form errors."""

    def to_python(self, value):
        if value and value.size > MAX_PHOTO_MB * 1024 * 1024:
            raise forms.ValidationError(
                f"Please choose a photo smaller than {MAX_PHOTO_MB} MB."
            )
        try:
            return super().to_python(value)
        except cloudinary.exceptions.Error:
            raise forms.ValidationError(
                "That file couldn't be uploaded. Please choose a JPG, PNG "
                "or WebP photo."
            )


class RingForm(forms.ModelForm):
    """Add a ring, with an optional photo that goes to Cloudinary."""

    image = PhotoField(
        label="Photo",
        required=False,
        options={"allowed_formats": ["jpg", "png", "webp"]},
        widget=forms.FileInput(attrs={"accept": "image/*"}),
        help_text=f"Optional. A JPG, PNG or WebP photo under {MAX_PHOTO_MB} "
        "MB. Until there is one, your ring shows a drawing of its style. "
        "When you edit a ring, leave this empty to keep its photo.",
    )

    class Meta:
        model = Ring
        fields = [
            "name",
            "style",
            "metal",
            "gemstone",
            "price",
            "description",
            "image",
        ]
        labels = {"price": "Price (£)"}
        help_texts = {
            "gemstone": "Solitaire, halo, trilogy and eternity rings need "
            "a gemstone.",
            "price": "The price in pounds: £1 or more.",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            # Phones show a number keypad with a decimal point.
            "price": forms.NumberInput(attrs={"inputmode": "decimal"}),
        }

    def clean(self):
        """A ring built around a stone needs a gemstone."""
        cleaned_data = super().clean()
        style = cleaned_data.get("style")
        gemstone = cleaned_data.get("gemstone")
        if style in STONE_STYLES and gemstone == Ring.Gemstone.NONE:
            style_name = Ring.Style(style).label
            self.add_error(
                "gemstone",
                f"{style_name} rings need a gemstone. Choose one, or "
                "change the style to Band.",
            )
        return cleaned_data
