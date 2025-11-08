from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("api/temps", views.fetch_temperatures, name="temps")
]
