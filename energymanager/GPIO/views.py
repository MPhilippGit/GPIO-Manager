from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import TemperatureValues

def index(request):
   return HttpResponse("Blub")

def fetch_temperatures(request):
   data = list(TemperatureValues.objects.values("measurement", "date"))
   return JsonResponse(data, safe=False)