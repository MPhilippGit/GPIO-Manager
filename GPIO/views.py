from energymanager.settings import BASE_DIR
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse, Http404
from .models import SensorValues

def index(request):
   template = loader.get_template("GPIO/dashboard.html")
   return HttpResponse(template.render({}, request))

def fetch_temperatures(request):
   data = list(SensorValues.objects.values("temperature", "timestamp", "is_plausible"))
   filter_data = data[-10:]
   return JsonResponse(filter_data, safe=False)

def fetch_humidities(request):
   data = list(SensorValues.objects.values("humidity", "timestamp", "is_plausible"))
   filter_data = data[-10:]
   return JsonResponse(filter_data, safe=False)

def fetch_vocs(request):
   data = list(SensorValues.objects.values("voc", "timestamp", "is_plausible"))
   filter_data = data[-10:]
   return JsonResponse(filter_data, safe=False)

def fetch_log(request):
   logfile = BASE_DIR / "app.log"
   logcontent = []
   with logfile.open("r") as f:
      for line in f.readlines()[::-3]:
         linefields = line.split("|")
         logcontent.append({
            "level": linefields[0].strip(),
            "timestamp": linefields[1].strip(),
            "content": linefields[2].strip()
         })
   return JsonResponse(logcontent, safe=False)