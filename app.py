# =============================================================================
# app.py - Flask Backend for AI-Based Diet Recommendation System
# =============================================================================
# This is the main web server file. It handles:
#   - Serving HTML pages (Home, Form, Result)
#   - Receiving user input from the form
#   - Loading the trained ML model
#   - Making diet predictions
#   - Returning results with BMI, diet type, calories, and meal plan
# =============================================================================

import pickle
import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, request

# -----------------------------------------------------------------------------
# Initialize Flask application
# Flask looks for templates in the 'templates/' folder automatically
# and static files in the 'static/' folder
# -----------------------------------------------------------------------------
app = Flask(__name__)

# -----------------------------------------------------------------------------
# Load the trained ML model and label encoder from pickle files
# These were created by running train_model.py
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(BASE_DIR, "label_encoder.pkl"), "rb") as f:
    label_encoder = pickle.load(f)

# -----------------------------------------------------------------------------
# Meal plans for each diet type
# These are returned to the user along with the ML prediction
# -----------------------------------------------------------------------------
MEAL_PLANS = {
    "Weight Loss": {
        "calories": "1200–1500 kcal/day",
        "breakfast": "Oatmeal with berries and green tea",
        "mid_morning": "Apple or a handful of almonds",
        "lunch": "Grilled chicken salad with lemon dressing",
        "evening": "Carrot & cucumber sticks with hummus",
        "dinner": "Steamed fish with vegetables and brown rice",
        "note": "Focus on high-fiber, low-calorie foods. Avoid sugary drinks and processed food.",
        "tips": [
            "Drink 8–10 glasses of water daily",
            "Avoid skipping meals — it slows metabolism",
            "Include 30 min of cardio (walking, jogging) daily",
            "Eat slowly and mindfully",
            "Limit refined carbs and fried food"
        ]
    },
    "Weight Gain": {
        "calories": "2500–3000 kcal/day",
        "breakfast": "Whole grain toast with peanut butter, banana, and a glass of full-fat milk",
        "mid_morning": "Mixed nuts, dried fruits, and a protein shake",
        "lunch": "Rice with lentils, paneer/chicken curry, and curd",
        "evening": "Whole grain crackers with cheese or avocado toast",
        "dinner": "Pasta or rice with egg/chicken, beans, and salad",
        "note": "Focus on nutrient-dense, calorie-rich foods. Eat frequent, large meals.",
        "tips": [
            "Eat every 2–3 hours throughout the day",
            "Include strength training (weights) 3–4 times/week",
            "Add healthy fats: nuts, avocado, olive oil",
            "Drink smoothies with milk, banana, and oats",
            "Prioritize sleep for muscle recovery"
        ]
    },
    "Maintain Weight": {
        "calories": "1800–2200 kcal/day",
        "breakfast": "Whole grain cereal with milk and seasonal fruits",
        "mid_morning": "Greek yogurt or a piece of fruit",
        "lunch": "Mixed grain rice with dal, vegetables, and salad",
        "evening": "Roasted seeds or a protein bar",
        "dinner": "Roti/bread with curry, vegetables, and a glass of milk",
        "note": "Maintain a balanced diet with all food groups in moderation.",
        "tips": [
            "Stay active with 30 min of moderate exercise daily",
            "Eat a rainbow of vegetables and fruits",
            "Balance macros: 50% carbs, 25% protein, 25% fats",
            "Monitor portion sizes to avoid overeating",
            "Stay consistent with meal timings"
        ]
    }
}


def calculate_bmi(weight, height):
    """
    Calculate BMI (Body Mass Index).
    Formula: BMI = weight(kg) / (height(m))^2
    """
    height_m = height / 100  # Convert cm to metres
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)


def get_bmi_category(bmi):
    """Return BMI category string based on BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


# -----------------------------------------------------------------------------
# Route: Home Page
# -----------------------------------------------------------------------------
@app.route("/")
def home():
    """Serve the home/landing page."""
    return render_template("index.html")


# -----------------------------------------------------------------------------
# Route: Input Form Page
# -----------------------------------------------------------------------------
@app.route("/form")
def form():
    """Serve the user input form page."""
    return render_template("form.html")


# -----------------------------------------------------------------------------
# Route: Handle Form Submission and Return Prediction
# -----------------------------------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    """
    Receive user inputs (age, weight, height) from the form,
    run the ML model to predict diet type, and render the result page.
    """
    try:
        # Step 1: Get form data from the POST request
        name = request.form.get("name", "").strip() or "Friend"
        age = float(request.form.get("age"))
        weight = float(request.form.get("weight"))
        height = float(request.form.get("height"))
        gender = request.form.get("gender", "Other")
        activity = request.form.get("activity", "Moderate")

        # Basic validation
        if not (1 <= age <= 120):
            raise ValueError("Age must be between 1 and 120.")
        if not (20 <= weight <= 300):
            raise ValueError("Weight must be between 20 and 300 kg.")
        if not (100 <= height <= 250):
            raise ValueError("Height must be between 100 and 250 cm.")

        # Step 2: Calculate BMI
        bmi = calculate_bmi(weight, height)
        bmi_category = get_bmi_category(bmi)

        # Step 3: Prepare input for ML model
        # The model expects: [Age, Weight, Height, BMI]
        # Use a DataFrame to preserve feature names and suppress sklearn warnings
        features = pd.DataFrame(
            [[age, weight, height, bmi]],
            columns=["Age", "Weight", "Height", "BMI"]
        )

        # Step 4: Make prediction using the trained Decision Tree model
        prediction_encoded = model.predict(features)[0]
        diet_type = label_encoder.inverse_transform([prediction_encoded])[0]

        # Step 5: Get prediction confidence/probabilities
        probabilities = model.predict_proba(features)[0]
        confidence = round(max(probabilities) * 100, 1)

        # Step 6: Adjust calorie recommendation based on gender & activity
        meal_plan = dict(MEAL_PLANS[diet_type])  # Copy so we can modify
        calorie_range = _adjust_calories(
            diet_type, gender, activity, weight, height, age
        )
        meal_plan["calories"] = calorie_range

        # Step 7: Render the result page with all data
        return render_template(
            "result.html",
            name=name,
            age=int(age),
            weight=weight,
            height=height,
            gender=gender,
            activity=activity,
            bmi=bmi,
            bmi_category=bmi_category,
            diet_type=diet_type,
            confidence=confidence,
            meal_plan=meal_plan,
        )

    except ValueError as e:
        return render_template("form.html", error=str(e))
    except Exception as e:
        return render_template("form.html", error=f"An error occurred: {str(e)}")


def _adjust_calories(diet_type, gender, activity, weight, height, age):
    """
    Calculate a personalised calorie target using the Mifflin-St Jeor equation.
    Returns a string like '1800–2000 kcal/day'.
    """
    # Base Metabolic Rate (BMR) — Mifflin-St Jeor equation
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == "Female":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 78  # Average

    # Activity multipliers
    activity_multipliers = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9,
    }
    multiplier = activity_multipliers.get(activity, 1.55)
    tdee = bmr * multiplier  # Total Daily Energy Expenditure

    # Adjust TDEE based on diet goal
    if diet_type == "Weight Loss":
        low = int(tdee - 500)
        high = int(tdee - 250)
    elif diet_type == "Weight Gain":
        low = int(tdee + 300)
        high = int(tdee + 500)
    else:  # Maintain
        low = int(tdee - 100)
        high = int(tdee + 100)

    return f"{low:,}–{high:,} kcal/day"


# -----------------------------------------------------------------------------
# Run the Flask development server
# Set the FLASK_DEBUG environment variable to enable debug mode:
#   export FLASK_DEBUG=1
# Never run with debug=True in a production environment.
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug_mode, port=5000)
