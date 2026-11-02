from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import generic
from django.views.decorators.http import require_POST

from .forms import RingForm
from .models import Favourite, Ring

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


def show_christmas_effect():
    """Return True in the Christmas season, 1 November to 6 January."""
    today = timezone.localdate()
    if today.month >= 11:
        return True
    if today.month == 1 and today.day <= 6:
        return True
    return False


def home(request):
    """The home page: the newest rings, every style and a few numbers."""
    rings = Ring.objects.order_by()
    counts = dict(rings.values_list("style").annotate(total=Count("id")))
    styles = [
        {
            "value": value,
            "label": label,
            "count": counts.get(value, 0),
            "image": f"images/styles/{value}.svg",
        }
        for value, label in Ring.Style.choices
    ]
    context = {
        "latest_rings": Ring.objects.all()[:3],
        "styles": styles,
        "ring_count": rings.count(),
        "collector_count": rings.values("owner").distinct().count(),
        "show_christmas_effect": show_christmas_effect(),
    }
    return render(request, "rings/index.html", context)


class RingList(generic.ListView):
    """The All rings page: every ring, nine rings a page.

    ?q=aurora shows only rings with "aurora" in their name, ?style=halo
    shows only halo rings, and ?sort=price_low sorts them by price.
    Values that don't exist, such as ?style=banana, are ignored.
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

    def get_search(self):
        """The words typed in the search box, without spaces at the ends."""
        return self.request.GET.get("q", "").strip()[:100]

    def get_sort(self):
        """The order chosen in the Sort menu, or "newest" if none is."""
        sort = self.request.GET.get("sort", "")
        if sort in SORT_OPTIONS:
            return sort
        return "newest"

    def get_queryset(self):
        rings = Ring.objects.all()
        search = self.get_search()
        if search:
            rings = rings.filter(name__icontains=search)
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
        context["q"] = self.get_search()
        return context


def ring_detail(request, slug):
    """One ring's own page, or the 404 page if no ring has that slug."""
    ring = get_object_or_404(Ring, slug=slug)
    is_favourite = (
        request.user.is_authenticated
        and ring.favourites.filter(user=request.user).exists()
    )
    context = {
        "ring": ring,
        "can_change": ring.can_be_changed_by(request.user),
        "is_favourite": is_favourite,
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


@login_required
@require_POST
def toggle_favourite(request, slug):
    """Save a ring to Favourites, or remove it if it's already saved."""
    ring = get_object_or_404(Ring, slug=slug)
    saved = Favourite.objects.filter(user=request.user, ring=ring)
    if saved.exists():
        saved.delete()
        messages.success(
            request, f"{ring.name} has been removed from your favourites."
        )
    else:
        Favourite.objects.create(user=request.user, ring=ring)
        messages.success(
            request, f"{ring.name} has been saved to your favourites."
        )
    # Go back to the page the button was on, but only on this website.
    next_url = request.POST.get("next", "")
    if url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)
    return redirect(ring)


@login_required
def favourites(request):
    """The rings the signed-in user has saved, newest saved first."""
    saved = request.user.favourites.select_related("ring")
    rings = [favourite.ring for favourite in saved]
    return render(request, "rings/favourites.html", {"rings": rings})
