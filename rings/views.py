from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic

from .forms import RingForm
from .models import Ring


def home(request):
    """The home page, with the three newest rings."""
    latest_rings = Ring.objects.all()[:3]
    return render(
        request, "rings/index.html", {"latest_rings": latest_rings}
    )


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
