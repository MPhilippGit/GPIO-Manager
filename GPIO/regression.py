import pandas as pd
from sklearn.linear_model import LinearRegression
from energymanager.settings import BASE_DIR
from sklearn.metrics import r2_score


class VOCRegressionModel:
    def __init__(self):
        self.df = pd.read_csv(BASE_DIR / "regression.csv")
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
