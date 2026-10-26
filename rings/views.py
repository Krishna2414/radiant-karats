from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .forms import RingForm
from .models import Ring


def home(request):
    rings = [
        {
            "name": "Solstice Solitaire",
            "detail": "Oval-cut moissanite · 14k gold",
            "price": "£489",
            "image": "https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=900&q=85",
            "alt": "Gold solitaire ring with a bright centre stone",
            "label": "Bestseller",
        },
        {
            "name": "The Heirloom",
            "detail": "Emerald-cut diamond · Platinum",
            "price": "£1,250",
            "image": "https://images.unsplash.com/photo-1603561591411-07134e71a2a9?auto=format&fit=crop&w=900&q=85",
            "alt": "Elegant engagement ring displayed close up",
            "label": "Made to order",
        },
        {
            "name": "Golden Hour Band",
            "detail": "Textured 18k recycled gold",
            "price": "£320",
            "image": "https://images.unsplash.com/photo-1603561596112-0a132b757442?auto=format&fit=crop&w=900&q=85",
            "alt": "Minimal gold ring with a polished finish",
            "label": "New",
        },
    ]
    return render(request, "rings/index.html", {"rings": rings})


class RingList(generic.ListView):
    """The All rings page: every ring, nine rings a page."""

    model = Ring
    template_name = "rings/ring_list.html"
    context_object_name = "rings"
    paginate_by = 9


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
