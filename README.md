# AI-Based Diet Recommendation System

A full-stack web application that uses **Machine Learning** to recommend a personalised diet plan based on your body metrics.

## 🚀 Features

- 🤖 **Decision Tree ML Model** — trained with scikit-learn to classify diet type
- 📊 **BMI Calculator** — instant Body Mass Index analysis with health category
- 🔥 **Personalised Calorie Target** — uses the Mifflin-St Jeor equation adjusted for gender & activity
- 🍽️ **Full Meal Plan** — breakfast-to-dinner daily plan tailored to your goal
- 💡 **Expert Nutrition Tips** — 5 actionable tips per diet type
- 📱 **Responsive UI** — works beautifully on mobile, tablet, and desktop
- 🖨️ **Print / Save** — print your plan or save as PDF

## 📂 Project Structure

```
Diet-Recommendation-System/
├── app.py               # Flask backend (routes + prediction logic)
├── train_model.py       # ML training script
├── dataset.csv          # Training dataset (Age, Weight, Height, Diet_Type)
├── model.pkl            # Trained Decision Tree model (auto-generated)
├── label_encoder.pkl    # Label encoder (auto-generated)
├── requirements.txt     # Python dependencies
├── templates/
│   ├── index.html       # Home / landing page
│   ├── form.html        # User input form
│   └── result.html      # Prediction results page
└── static/
    ├── css/style.css    # Stylesheet
    └── js/script.js     # Client-side interactivity
```

## 🛠️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Akrassum/Diet-Recommendation-System.git
cd Diet-Recommendation-System
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the ML model
```bash
python train_model.py
```
This generates `model.pkl` and `label_encoder.pkl`.

### 4. Run the Flask web server
```bash
python app.py
```

### 5. Open your browser
Visit **http://127.0.0.1:5000**

## 🧠 Machine Learning Details

| Component | Details |
|-----------|---------|
| Algorithm | Decision Tree Classifier |
| Features | Age, Weight (kg), Height (cm), BMI |
| Target | Diet Type (Weight Loss / Weight Gain / Maintain Weight) |
| Training Accuracy | 100% (clean, structured dataset) |
| Library | scikit-learn |

### How the model works:
1. User provides **Age**, **Weight**, **Height**, **Gender**, and **Activity Level**
2. **BMI** is calculated: `BMI = weight / (height/100)²`
3. The Decision Tree classifies the input into one of 3 diet categories
4. **Calorie target** is computed using the Mifflin-St Jeor equation × activity multiplier
5. A matching **meal plan and tips** are returned

## 🍽️ Diet Categories

| Category | BMI Range | Calorie Approach |
|----------|-----------|-----------------|
| Weight Loss | ≥ 25 | Calorie deficit (−250 to −500 kcal) |
| Maintain Weight | 18.5–24.9 | Maintenance calories |
| Weight Gain | < 18.5 | Calorie surplus (+300 to +500 kcal) |

## ⚠️ Disclaimer

This tool is for **informational and educational purposes only**.  
Always consult a registered dietitian or healthcare professional before making significant dietary changes.

---
Built with ❤️ using **Flask** + **scikit-learn** + **HTML/CSS/JS**
