import pickle
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

# Load the fitted model and preprocessor
MODELS_DIR = BASE_DIR / "models"
with open(MODELS_DIR / "random_forest_model.pkl", "rb") as file:
    model = pickle.load(file)

with open(MODELS_DIR / "preprocessor.pkl", "rb") as file:
    preprocessor = pickle.load(file)


@app.route("/", methods=["GET", "POST"])
def predict():
    prediction = None

    if request.method == "POST":
        # These names and values must match the fields in your HTML form.
        car_data = pd.DataFrame([{
            "model": request.form["model"],
            "vehicle_age": int(request.form["vehicle_age"]),
            "km_driven": float(request.form["km_driven"]),
            "seller_type": request.form["seller_type"],
            "fuel_type": request.form["fuel_type"],
            "transmission_type": request.form["transmission_type"],
            "mileage": float(request.form["mileage"]),
            "engine": float(request.form["engine"]),
            "max_power": float(request.form["max_power"]),
            "seats": int(request.form["seats"]),
        }])

        processed_data = preprocessor.transform(car_data)
        prediction = model.predict(processed_data)[0]
        prediction = f"₹{prediction:,.0f}"

    return render_template("index.html", prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)