from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("api/temps", views.fetch_temperatures, name="temps"),
    path("api/humids", views.fetch_humidities, name="humids"),
    path("api/vocs", views.fetch_vocs, name="vocs"),
    path("logs", views.fetch_log, name="log")
]
