from energymanager.settings import BASE_DIR
from django.shortcuts import render
from django.template import loader
from django.db.models import F
from django.http import HttpResponse, JsonResponse, Http404
from .models import SensorValues
from .regression import VOCRegressionModel, TemperatureRegressionModel
import csv

def index(request):
   template = loader.get_template("GPIO/dashboard.html")
   return HttpResponse(template.render({}, request))

def fetch_temperatures(request):
   data = list(SensorValues.objects.annotate(
      measurement=F("temperature")
   ).values("measurement", "timestamp", "is_plausible"))
   filter_data = data[-10:]
   return JsonResponse(filter_data, safe=False)

def fetch_humidities(request):
   data = list(SensorValues.objects.annotate(
      measurement=F("temperature")
   ).values("measurement", "timestamp", "is_plausible"))
   filter_data = data[-10:]
   return JsonResponse(filter_data, safe=False)

def fetch_vocs(request):
   data = list(SensorValues.objects.annotate(
      measurement=F("voc")
   ).values("measurement", "timestamp", "is_plausible"))
   filter_data = data[-10:]
   return JsonResponse(filter_data, safe=False)

def fetch_latest(request):
   data = SensorValues.objects.latest("timestamp")
   result = {
      "temperature": data.temperature,
      "humidity": data.humidity,
      "voc": data.voc,
      "pressure": data.pressure,
      "is_plausible": data.is_plausible,
      "timestamp": data.timestamp
   }
   return JsonResponse(result, safe=False)

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

def fetch_training_data(request):
   training_data = BASE_DIR / "trainingdata" / "basedata.csv"
   result = []
   with training_data.open("r") as file:
      file_data = csv.DictReader(file)
      
      for data_row in file_data:
         result.append(data_row)
   
   return JsonResponse(result, safe=False)

def predict_persons(request):
   model = VOCRegressionModel()
   result = {
      "model": {
         "slope": model.get_slope(),
         "intercept": model.get_intercept(),
         "r2_score": model.get_r2_scrore()
      },
      "data": model.get_training_data()
   }
   return JsonResponse(result, safe=False)

def predict_temperature(request, temp_value):
   model = TemperatureRegressionModel()
   result = model.predict(temp_value)
   return JsonResponse(result, safe=False)