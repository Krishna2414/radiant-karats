from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import generic

from .forms import RingForm
from .models import Ring

# The Sort menu on All rings: the value in the address, then the label.
SORT_OPTIONS = {
    "newest": "Newest first",
    "price_low": "Price: low to high",
    "price_high": "Price: high to low",
}

# How each choice orders the rings. Rings with the same price stay
# newest first, so they never swap places between pages.
SORT_ORDERS = {
    "newest": ["-created_on"],
    "price_low": ["price", "-created_on"],
    "price_high": ["-price", "-created_on"],
}


def show_halloween_effect():
    """Return True during the Halloween season, inclusive of Oct 24 to Nov 1."""
    today = timezone.localdate()
    if today.month == 10 and today.day >= 24:
        return True
    if today.month == 11 and today.day <= 1:
        return True
    return False


def home(request):
    """The home page, with the three newest rings."""
    latest_rings = Ring.objects.all()[:3]
    return render(
        request,
        "rings/index.html",
        {
            "latest_rings": latest_rings,
            "show_halloween_effect": show_halloween_effect(),
        },
    )


class RingList(generic.ListView):
    """The All rings page: every ring, nine rings a page.

    ?style=halo shows only halo rings, and ?sort=price_low sorts them by
    price. Values that don't exist, such as ?style=banana, are ignored.
    """

    model = Ring
    template_name = "rings/ring_list.html"
    context_object_name = "rings"
    paginate_by = 9

    def get_style(self):
        """The style chosen in the Style menu, or "" for every style."""
        style = self.request.GET.get("style", "")
        if style in Ring.Style.values:
            return style
        return ""

    def get_sort(self):
        """The order chosen in the Sort menu, or "newest" if none is."""
        sort = self.request.GET.get("sort", "")
        if sort in SORT_OPTIONS:
            return sort
        return "newest"

    def get_queryset(self):
        rings = Ring.objects.all()
        style = self.get_style()
        if style:
            rings = rings.filter(style=style)
        return rings.order_by(*SORT_ORDERS[self.get_sort()])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        style = self.get_style()
        context["style"] = style
        context["style_name"] = Ring.Style(style).label if style else ""
        context["styles"] = Ring.Style.choices
        context["sort"] = self.get_sort()
        context["sort_options"] = SORT_OPTIONS
        return context


def ring_detail(request, slug):
    """One ring's own page, or the 404 page if no ring has that slug."""
    ring = get_object_or_404(Ring, slug=slug)
    context = {
        "ring": ring,
        "can_change": ring.can_be_changed_by(request.user),
    }
    return render(request, "rings/ring_detail.html", context)


@login_required
def ring_create(request):
    """Add a new ring. The signed-in user becomes its owner."""
    if request.method == "POST":
        form = RingForm(request.POST, request.FILES)
        if form.is_valid():
            ring = form.save(commit=False)
            ring.owner = request.user
            ring.save()
            messages.success(request, f"{ring.name} has been added.")
            return redirect(ring)
        messages.error(request, "Please check the form for errors.")
    else:
        form = RingForm()
    return render(request, "rings/ring_form.html", {"form": form})


@login_required
def ring_edit(request, slug):
    """Edit a ring. Only its owner, or staff, may do this."""
    ring = get_object_or_404(Ring, slug=slug)
    if not ring.can_be_changed_by(request.user):
        raise PermissionDenied
    if request.method == "POST":
        form = RingForm(request.POST, request.FILES, instance=ring)
        if form.is_valid():
            form.save()
            messages.success(request, f"{ring.name} has been updated.")
            return redirect(ring)
        messages.error(request, "Please check the form for errors.")
    else:
        form = RingForm(instance=ring)
    context = {"form": form, "ring": ring}
    return render(request, "rings/ring_form.html", context)


@login_required
def ring_delete(request, slug):
    """Delete a ring, but only on a POST. Only its owner, or staff."""
    ring = get_object_or_404(Ring, slug=slug)
    if not ring.can_be_changed_by(request.user):
        raise PermissionDenied
    if request.method == "POST":
        ring.delete()
        messages.success(request, f"{ring.name} has been deleted.")
        if ring.owner == request.user:
            return redirect("my_rings")
        return redirect("ring_list")
    return render(request, "rings/ring_confirm_delete.html", {"ring": ring})


@login_required
def my_rings(request):
    """The signed-in user's own rings, newest first."""
    rings = request.user.rings.all()
    return render(request, "rings/my_rings.html", {"rings": rings})
