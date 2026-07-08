"""
app.py
------
Flask web application for the Human Development Index (HDI) Prediction
System.

Routes:
    /            -> Home page (project introduction)
    /predict     -> Prediction page (GET: show form, POST: run model)

The trained Linear Regression model (HDI.pkl), the country LabelEncoder
(country_encoder.pkl), and the country dropdown list (countries_list.pkl)
are all produced by Training/HumDevIndex.ipynb and must live in this same
Flask/ folder for the app to run.
"""

import pickle
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Load trained model + supporting artifacts once, at startup
# ---------------------------------------------------------------------------
model = pickle.load(open("HDI.pkl", "rb"))
country_encoder = pickle.load(open("country_encoder.pkl", "rb"))
countries = pickle.load(open("countries_list.pkl", "rb"))


def categorize_hdi(score):
    """Map a numeric HDI score to its official UNDP tier."""
    if score >= 0.800:
        return "Very High"
    elif score >= 0.700:
        return "High"
    elif score >= 0.550:
        return "Medium"
    else:
        return "Low"


@app.route("/")
def home():
    """Home page: introduces the HDI project."""
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
    GET  -> render the input form (indexnew.html) with the country dropdown
    POST -> read form values, run the model, and render the result
    """
    if request.method == "GET":
        return render_template("indexnew.html", countries=countries, result=None)

    try:
        country = request.form["country"]
        life_expectancy = float(request.form["life_expectancy"])
        mean_years_schooling = float(request.form["mean_years_schooling"])
        expected_years_schooling = float(request.form["expected_years_schooling"])
        gni_per_capita = float(request.form["gni_per_capita"])
        internet_users_pct = float(request.form["internet_users_pct"])

        country_encoded = country_encoder.transform([country])[0]

        features = np.array([[
            country_encoded,
            life_expectancy,
            mean_years_schooling,
            expected_years_schooling,
            gni_per_capita,
            internet_users_pct,
        ]])

        predicted_score = float(model.predict(features)[0])
        predicted_score = round(max(0.0, min(1.0, predicted_score)), 3)
        category = categorize_hdi(predicted_score)

        result = {
            "score": predicted_score,
            "category": f"{category} HDI",
        }
        return render_template(
            "indexnew.html", countries=countries, result=result, selected_country=country
        )

    except Exception as e:
        error = f"Something went wrong while predicting: {e}"
        return render_template("indexnew.html", countries=countries, result=None, error=error)


if __name__ == "__main__":
    app.run(debug=True)
