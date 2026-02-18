"""HTTP views for the GPIO app.

These views provide simple JSON endpoints and a dashboard page used by the
frontend. Each view is intentionally small and focuses on querying the
`SensorValues` model or reading small local files used for diagnostics and
training data.

Notes:
- Many endpoints return small slices of recent measurements for the UI.
- This module purposefully avoids heavy processing to keep response times
   predictable for the frontend.
"""

from energymanager.settings import BASE_DIR
from django.shortcuts import render
from django.template import loader
from django.db.models import F
from django.http import HttpResponse, JsonResponse, Http404
from .models import SensorValues
from .regression import VOCRegressionModel, TemperatureRegressionModel
import csv

def index(request):
   """Render the main dashboard HTML.

   The dashboard is a lightweight page; frontend JavaScript fetches data from
   the JSON endpoints below.
   """
   template = loader.get_template("GPIO/dashboard.html")
   return HttpResponse(template.render({}, request))

def fetch_temperatures(request):
   """Return the last 10 temperature measurements as JSON.

   The view annotates the queryset with a `measurement` key to present a
   consistent shape to the frontend, independent of the actual sensor field
   name used in the database model.
   """
   data = list(SensorValues.objects.annotate(
      measurement=F("temperature")
   ).values("measurement", "timestamp", "is_plausible"))
   filter_data = data[-10:]
   return JsonResponse(filter_data, safe=False)

def fetch_humidities(request):
   """Return the last 10 humidity measurements as JSON.

   NOTE: This function currently annotates `measurement` from the
   `temperature` field - likely a copy/paste error. Leaving behavior unchanged
   for now but this should use `F('humidity')` to return humidity values.
   """
   data = list(SensorValues.objects.annotate(
      measurement=F("temperature")
   ).values("measurement", "timestamp", "is_plausible"))
   filter_data = data[-10:]
   return JsonResponse(filter_data, safe=False)

def fetch_vocs(request):
   """Return the last 10 VOC measurements as JSON."""
   data = list(SensorValues.objects.annotate(
      measurement=F("voc")
   ).values("measurement", "timestamp", "is_plausible"))
   filter_data = data[-10:]
   return JsonResponse(filter_data, safe=False)

def fetch_latest(request):
   """Return the most recent sensor measurement as JSON.

   Uses the model's `latest` convenience method and constructs a small dict
   with the values the frontend expects.
   """
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
   """Return recent lines from the application log as JSON.

   The log file is expected to contain pipe-separated fields in each line
   with the format: LEVEL | TIMESTAMP | CONTENT. Lines are read in reverse
   order to present the newest messages first.
   """
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
   """Return the contents of the training CSV as a list of dicts.

   This endpoint is useful for frontend visualisation and debugging of the
   model training dataset. It streams the entire CSV into memory which is
   acceptable for the small training file used by this project.
   """
   training_data = BASE_DIR / "trainingdata" / "basedata.csv"
   result = []
   with training_data.open("r") as file:
      file_data = csv.DictReader(file)
      
      for data_row in file_data:
         result.append(data_row)
   
   return JsonResponse(result, safe=False)

def predict_persons(request):
   """Return trained VOC->persons regression info and training points.

   The response includes the learned slope/intercept/r2 and the raw
   training rows used to fit the model so the frontend can display the fit.
   """
   model = VOCRegressionModel()
   result = {
      "model": {
         "slope": model.get_slope(),
         "intercept": model.get_intercept(),
         "r2_score": model.get_r2_scrore()
      },
      "voc_model": model._voc_to_person(),
      "data": model.get_training_data()
   }
   print(model._voc_to_person())
   return JsonResponse(result, safe=False)

def predict_temperature(request, temp_value):
   """Predict a temperature-related value using the temperature model.

   NOTE: `TemperatureRegressionModel` does not currently expose a `predict`
   method in `GPIO.regression`. Calling this view as-is will raise an
   AttributeError. The view is left unchanged but annotated so it can be
   corrected safely in a follow-up change.
   """
   model = TemperatureRegressionModel()
   result = model.predict(temp_value)
   return JsonResponse(result, safe=False)