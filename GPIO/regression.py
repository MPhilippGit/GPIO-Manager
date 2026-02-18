"""Regression helpers for mapping VOC sensor values to targets.

This module provides small linear regression wrappers used by the
application to predict estimated person counts and temperatures from
VOC sensor readings. It also contains a simple CSV export helper for
training data.

Notes:
- Models are trained on the CSV file located in `trainingdata/basedata.csv`.
- Methods intentionally preserve existing public names (even if misspelled)
  to avoid breaking external callers.
"""

import pandas as pd
import csv
from sklearn.linear_model import LinearRegression
from energymanager.settings import BASE_DIR
from sklearn.metrics import r2_score
from GPIO.models import SensorValues, SensorCSVExporter


class VOCRegressionModel:
    """Linear model predicting estimated persons from VOC values.

    Attributes:
        FILE_REFERENCE: Path to the CSV file used to load training data.
        df: pandas DataFrame loaded from the CSV on initialization.
        model: Fitted `LinearRegression` instance.
        r2_score: Coefficient of determination for the fit.
    """

    FILE_REFERENCE = BASE_DIR / "trainingdata" / "basedata.csv"

    def __init__(self):
        # Load training data and train the model immediately.
        self.df = pd.read_csv(self.FILE_REFERENCE)
        self.model = LinearRegression()
        self.r2_score = None
        self._train()

    def _train(self):
        X = self.df[['persons_estimated']]
        y = self.df['temperature']

        # Fit the linear model on the whole dataset.
        self.model.fit(X, y)

        # Compute predictions on the training set and store R^2 score.
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
        # Returns the stored R^2 score (method name kept for compatibility).
        return self.r2_score

    def get_slope(self):
        # Return the learned coefficient (slope) for the single-feature model.
        return self.model.coef_[0]

    def get_intercept(self):
        # Return the learned intercept of the linear model.
        return self.model.intercept_

    def get_training_data(self):
        """Read the CSV file and return a list of simple dicts for UI display.

        Each item contains the original VOC value and the target persons value.
        """
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
    """Linear model predicting temperature from VOC values.

    This class mirrors `VOCRegressionModel` but uses `temperature` as the
    target column. The API is intentionally similar to keep usage consistent.
    """

    def __init__(self):
        # Read the same training CSV used by VOCRegressionModel.
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
        # Return the stored R^2 score for the temperature model.
        return self.r2_score

    def get_slope(self):
        return self.model.coef_[0]

    def get_intercept(self):
        return self.model.intercept_

    def predict_temperature(self, person_amount):
        prediction = self.model.predict([[person_amount]])[0]

class TrainingDataExporter:

class TrainingData:
    """Export plausible sensor readings to a CSV file for training.

    Attributes:
        file: Path where the exported CSV is written.
        override: Placeholder flag for potential future behavior.
    """

    file = BASE_DIR / "trainingdata" / "trained.csv"
    override = False

    def __init__(self):
        # Query only plausible measurements from the database.
        self.data = SensorValues.objects.filter(is_plausible=1).all()

    def ensure_file_exists(self):
        if not TrainingDataExporter.file.exists():
            self.file.touch()

    def write_csv(self):
        # Write the queried sensor rows into `self.file` using the
        # `SensorCSVExporter` helper to produce consistent headers/rows.
        with self.file.open("w") as file:
            fieldnames = SensorCSVExporter.HEADERS
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            for entry in self.data:
                writer.writerow(SensorCSVExporter.row(entry))


