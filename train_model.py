"""
train_model.py
--------------
Trains a Decision Tree Classifier to predict diet type based on
Age, Weight, and Height features, then saves the trained model
using pickle so Flask can load it at runtime.

Run this script once before starting the Flask app:
    python train_model.py
"""

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

# ── 1. Load dataset ───────────────────────────────────────────────────────────
df = pd.read_csv("diet_data.csv")

# ── 2. Features and target ────────────────────────────────────────────────────
# We use Age, Weight (kg), Height (cm) to predict Diet_Type
X = df[["Age", "Weight", "Height"]]
y = df["Diet_Type"]

# ── 3. Train / test split ─────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── 4. Train Decision Tree Classifier ─────────────────────────────────────────
# max_depth=5 keeps the tree shallow enough to avoid overfitting
clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# ── 5. Evaluate model ─────────────────────────────────────────────────────────
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ── 6. Save model to disk ─────────────────────────────────────────────────────
with open("diet_model.pkl", "wb") as f:
    pickle.dump(clf, f)

print("\nModel saved successfully as 'diet_model.pkl'")
