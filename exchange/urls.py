from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("usd-uah/", views.usd_uah, name="usd-uah"),
    path("eur-uah/", views.eur_uah, name="eur-uah"),
    path("uah-usd/", views.uah_usd, name="uah-usd"),
    path("uah-eur/", views.uah_eur, name="uah-eur"),
]
