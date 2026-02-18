import pandas as pd
import csv
from sklearn.linear_model import LinearRegression
from energymanager.settings import BASE_DIR
from sklearn.metrics import r2_score
from GPIO.models import SensorValues, SensorCSVExporter


class VOCRegressionModel:
    FILE_REFERENCE = BASE_DIR / "trainingdata" / "basedata.csv"

    """
    Builds a model that can predict the amount of persons based on the voc data
    """
    def __init__(self):
        self.df = pd.read_csv(self.FILE_REFERENCE)
        self.model = LinearRegression()
        self.r2_score = None
        self._train()

    def _train(self):
        X = self.df[['persons_estimated']]
        y = self.df['temperature']

        self.model.fit(X, y)

        y_pred = self.model.predict(X)
        self.r2_score = r2_score(y, y_pred)
        return self

    def _voc_to_person(self):
        X = self.df[['voc_value']]
        y = self.df['persons_estimated']

        self.person_model = LinearRegression()
        self.person_model.fit(X, y)
        self.person_model.predict(X)

        return {
            "slope": self.person_model.coef_[0],
            "intercept": self.person_model.intercept_
        }

    def get_r2_scrore(self):
        return self.r2_score

    def get_slope(self):
        return self.model.coef_[0]

    def get_intercept(self):
        return self.model.intercept_

    def get_training_data(self):
        training_data = []
        with self.FILE_REFERENCE.open("r") as file:
            file_data = csv.DictReader(file)
            
            for data_row in file_data:
                training_data.append({
                    "source": data_row["persons_estimated"],
                    "target": data_row["temperature"]
                })
        return training_data

class TemperatureRegressionModel:
    """
    Builds a model that can predict temperatures based on the voc data
    """
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

    def get_r2_scrore(self):
        return self.r2_score

    def get_slope(self):
        return self.model.coef_[0]

    def get_intercept(self):
        return self.model.intercept_

    def predict_temperature(self, person_amount):
        prediction = self.model.predict([[person_amount]])[0]

class TrainingDataExporter:
    file = BASE_DIR / "trainingdata" / "trained.csv"
    override = False

    def __init__(self):
        self.data = SensorValues.objects.filter(is_plausible=1).all()

    def ensure_file_exists(self):
        if not TrainingDataExporter.file.exists():
            self.file.touch()

    def write_csv(self):
        with self.file.open("w") as file:
            fieldnames = SensorCSVExporter.HEADERS
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            for entry in self.data:
                writer.writerow(SensorCSVExporter.row(entry))


