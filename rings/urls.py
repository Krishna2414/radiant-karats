from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("rings/", views.RingList.as_view(), name="ring_list"),
    path("rings/add/", views.ring_create, name="ring_create"),
    path("rings/mine/", views.my_rings, name="my_rings"),
    path("rings/<slug:slug>/", views.ring_detail, name="ring_detail"),
    path("rings/<slug:slug>/edit/", views.ring_edit, name="ring_edit"),
    path("rings/<slug:slug>/delete/", views.ring_delete, name="ring_delete"),
]
