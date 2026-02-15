import pandas as pd
import csv
from sklearn.linear_model import LinearRegression
from energymanager.settings import BASE_DIR
from sklearn.metrics import r2_score
from GPIO.models import SensorValues, SensorCSVExporter


class VOCRegressionModel:
    def __init__(self):
        self.df = pd.read_csv(BASE_DIR / "trainingdata" / "basedata.csv")
        self.model = LinearRegression()
        self.r2_score = None
        self._train()

    def _train(self):
        X = self.df[['voc_value']]
        y = self.df['persons_estimated']

        self.model.fit(X, y)

        y_pred = self.model.predict(X)
        self.r2_score = r2_score(y, y_pred)

    def predict(self, voc_value: float) -> dict:
        prediction = self.model.predict([[voc_value]])[0]

        return {
            "voc": voc_value,
            "predicted": round(prediction),
            "r2_score": round(self.r2_score, 4)
        }

class TemperatureRegressionModel:
    def __init__(self):
        self.df = pd.read_csv(BASE_DIR / "trainingdata" / "basedata.csv")
        self.model = LinearRegression()
        self.r2_score = None
        self._train()

    def _train(self):
        X = self.df[['voc_value']]
        y = self.df['temperature']

        self.model.fit(X, y)

        y_pred = self.model.predict(X)
        self.r2_score = r2_score(y, y_pred)

    def predict(self, voc_value: float) -> dict:
        prediction = self.model.predict([[voc_value]])[0]

        return {
            "voc": voc_value,
            "predicted": round(prediction),
            "r2_score": round(self.r2_score, 4)
        }

class TrainingData:
    file = BASE_DIR / "trainingdata" / "trained.csv"
    override = False

    def __init__(self):
        self.data = SensorValues.objects.filter(is_plausible=1).all()

    def ensure_file_exists(self):
        if not TrainingData.file.exists():
            self.file.touch()

    def write_csv(self):
        with self.file.open("w") as file:
            fieldnames = SensorCSVExporter.HEADERS
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            for entry in self.data:
                writer.writerow(SensorCSVExporter.row(entry))


