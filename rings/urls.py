from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("rings/", views.RingList.as_view(), name="ring_list"),
    path("rings/<slug:slug>/", views.ring_detail, name="ring_detail"),
]
