import joblib
import numpy as np

# Load trained model
model = joblib.load("diabetes_model.pkl")


def predict_diabetes(data):

    features = np.array([
        data["pregnancies"],
        data["glucose"],
        data["blood_pressure"],
        data["skin_thickness"],
        data["insulin"],
        data["bmi"],
        data["pedigree"],
        data["age"]
    ]).reshape(1, -1)

    prediction = model.predict(features)[0]

    probability = model.predict_proba(features)[0][1]

    return prediction, probability