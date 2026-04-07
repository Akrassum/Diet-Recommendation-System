"""
app.py
------
Flask backend for the AI-Based Diet Recommendation System.

Routes:
    GET  /           → Home page
    GET  /form       → Input form page
    POST /predict    → Run ML prediction and display results
    GET  /about      → About page (optional)

Run the app:
    python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import pickle
import os

app = Flask(__name__)

# ── Load trained model ────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "diet_model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "diet_model.pkl not found. Please run 'python train_model.py' first."
    )

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# ── Helper functions ──────────────────────────────────────────────────────────

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Return BMI rounded to one decimal place."""
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


def bmi_category(bmi: float) -> str:
    """Return a human-readable BMI category."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal weight"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"


def calorie_recommendation(diet_type: str, weight_kg: float, height_cm: float, age: int) -> dict:
    """
    Return daily calorie target and a sample meal plan based on diet type.
    Uses a simplified Mifflin-St Jeor equation (assumes moderately active).
    """
    # Base metabolic rate (simplified, gender-neutral average)
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    tdee = round(bmr * 1.55)  # moderately active multiplier

    if diet_type == "Weight Loss":
        calories = tdee - 500
        meal_plan = {
            "Breakfast": "Oats with skimmed milk, 1 boiled egg, green tea",
            "Mid-Morning Snack": "A handful of almonds or 1 apple",
            "Lunch": "Grilled chicken / paneer salad, 2 chapatis, dal, vegetables",
            "Evening Snack": "Low-fat yogurt or a small fruit",
            "Dinner": "Steamed fish / tofu, brown rice or 1 chapati, vegetable soup",
            "Hydration": "Drink at least 8–10 glasses of water daily",
        }
    elif diet_type == "Weight Gain":
        calories = tdee + 500
        meal_plan = {
            "Breakfast": "Banana smoothie with full-fat milk, 3 scrambled eggs, whole-grain toast",
            "Mid-Morning Snack": "Peanut butter on whole-grain crackers, a glass of milk",
            "Lunch": "Rice with dal, paneer / chicken curry, vegetables, curd",
            "Evening Snack": "Dry fruits and nuts mix, protein shake",
            "Dinner": "Whole-wheat pasta / rice, grilled chicken / lentils, mixed vegetables",
            "Hydration": "Drink at least 8 glasses of water; include milk and fresh juices",
        }
    else:  # Maintain Weight
        calories = tdee
        meal_plan = {
            "Breakfast": "Whole-grain cereal or upma, 1 boiled egg, fresh fruit",
            "Mid-Morning Snack": "Mixed nuts or a fruit",
            "Lunch": "2 chapatis, dal, vegetable sabzi, curd",
            "Evening Snack": "Sprouts chaat or a glass of buttermilk",
            "Dinner": "Brown rice / 2 chapatis, grilled fish / tofu, mixed vegetable curry",
            "Hydration": "Drink at least 8 glasses of water daily",
        }

    return {"calories": calories, "meal_plan": meal_plan}


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        age = int(request.form["age"])
        weight = float(request.form["weight"])
        height = float(request.form["height"])

        # Validate ranges
        if not (1 <= age <= 120):
            raise ValueError("Age must be between 1 and 120.")
        if not (10 <= weight <= 300):
            raise ValueError("Weight must be between 10 and 300 kg.")
        if not (50 <= height <= 250):
            raise ValueError("Height must be between 50 and 250 cm.")

        # Calculate BMI
        bmi = calculate_bmi(weight, height)
        bmi_cat = bmi_category(bmi)

        # Predict diet type using the ML model
        # Use a DataFrame so the model receives correct feature names
        input_df = pd.DataFrame(
            [[age, weight, height]], columns=["Age", "Weight", "Height"]
        )
        prediction = model.predict(input_df)[0]

        # Calorie recommendation and meal plan
        rec = calorie_recommendation(prediction, weight, height, age)

        return render_template(
            "result.html",
            age=age,
            weight=weight,
            height=height,
            bmi=bmi,
            bmi_category=bmi_cat,
            diet_type=prediction,
            calories=rec["calories"],
            meal_plan=rec["meal_plan"],
        )

    except (ValueError, KeyError) as e:
        error_msg = str(e) if str(e) else "Invalid input. Please check your values."
        return render_template("form.html", error=error_msg)


if __name__ == "__main__":
    app.run(debug=True)
