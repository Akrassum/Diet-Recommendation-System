# AI-Based Diet Recommendation System

A full-stack web application that uses a **Decision Tree Classifier** (scikit-learn) to predict a personalised diet plan based on your age, weight, and height.

## Features

- **BMI Calculation** with weight-status classification
- **ML Prediction** — Diet Type: Weight Loss / Weight Gain / Maintain Weight
- **Calorie Target** computed from body metrics
- **Daily Meal Plan** tailored to your predicted diet type
- **Responsive UI** — works on desktop and mobile
- **Live BMI Preview** on the input form

## Project Structure

```
Diet-Recommendation-System/
├── app.py              # Flask backend
├── train_model.py      # ML training script
├── diet_data.csv       # Dataset (Age, Weight, Height, Diet_Type)
├── requirements.txt    # Python dependencies
├── templates/
│   ├── index.html      # Home page
│   ├── form.html       # Input form
│   └── result.html     # Results / diet plan
└── static/
    ├── style.css       # Stylesheet
    └── script.js       # Frontend interactivity
```

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the ML model

Run this once to generate `diet_model.pkl`:

```bash
python train_model.py
```

### 3. Start the Flask app

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## How It Works

1. The user enters their **age**, **weight (kg)**, and **height (cm)** on the form page.
2. The Flask backend calculates the **BMI** and passes the three features to the trained Decision Tree model.
3. The model predicts one of three **diet types**: *Weight Loss*, *Weight Gain*, or *Maintain Weight*.
4. A personalised **daily calorie target** and **meal plan** are computed and displayed on the results page.

## ML Model Details

| Detail | Value |
|--------|-------|
| Algorithm | Decision Tree Classifier |
| Features | Age, Weight (kg), Height (cm) |
| Target | Diet_Type (3 classes) |
| Test Accuracy | ~90% |
| Library | scikit-learn |