# =============================================================================
# train_model.py - ML Model Training Script
# =============================================================================
# This script trains a Decision Tree Classifier to predict diet type
# based on user inputs: Age, Weight (kg), Height (cm).
#
# The model learns patterns from a CSV dataset and saves the trained model
# as a .pkl (pickle) file so that Flask can load and use it for predictions.
# =============================================================================

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# -----------------------------------------------------------------------------
# Step 1: Load the dataset
# The CSV has columns: Age, Weight, Height, Diet_Type
# -----------------------------------------------------------------------------
dataset_path = os.path.join(os.path.dirname(__file__), "dataset.csv")
df = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")
print(f"Shape: {df.shape}")
print("\nSample rows:")
print(df.head())
print("\nDiet type distribution:")
print(df["Diet_Type"].value_counts())

# -----------------------------------------------------------------------------
# Step 2: Feature Engineering
# We add BMI as an extra feature because BMI strongly correlates with
# recommended diet type (underweight → gain, overweight → loss).
# BMI = Weight(kg) / (Height(m))^2
# -----------------------------------------------------------------------------
df["BMI"] = df["Weight"] / ((df["Height"] / 100) ** 2)
df["BMI"] = df["BMI"].round(2)

print("\nBMI statistics:")
print(df["BMI"].describe())

# -----------------------------------------------------------------------------
# Step 3: Prepare features (X) and target (y)
# Features: Age, Weight, Height, BMI
# Target:   Diet_Type (categorical string → encoded as integer)
# -----------------------------------------------------------------------------
feature_columns = ["Age", "Weight", "Height", "BMI"]
X = df[feature_columns]
y = df["Diet_Type"]

# Encode the target labels so the model can handle them
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print(f"\nClasses: {label_encoder.classes_}")
print(f"Encoded values: {list(range(len(label_encoder.classes_)))}")

# -----------------------------------------------------------------------------
# Step 4: Split dataset into training and testing sets
# 80% training data, 20% testing data
# random_state ensures reproducibility
# -----------------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")

# -----------------------------------------------------------------------------
# Step 5: Train the Decision Tree Classifier
# Decision Tree is a simple, interpretable ML algorithm.
# max_depth limits the tree to avoid overfitting.
# -----------------------------------------------------------------------------
model = DecisionTreeClassifier(
    max_depth=5,          # Limit depth to prevent overfitting
    random_state=42,      # Reproducibility
    min_samples_split=4,  # Minimum samples required to split a node
    min_samples_leaf=2    # Minimum samples required at a leaf node
)

model.fit(X_train, y_train)
print("\nModel training complete!")

# -----------------------------------------------------------------------------
# Step 6: Evaluate the model on the test set
# -----------------------------------------------------------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(
    y_test, y_pred, target_names=label_encoder.classes_
))

# -----------------------------------------------------------------------------
# Step 7: Save the trained model and label encoder using pickle
# This allows Flask to load the model without retraining every time.
# -----------------------------------------------------------------------------
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
encoder_path = os.path.join(os.path.dirname(__file__), "label_encoder.pkl")

with open(model_path, "wb") as f:
    pickle.dump(model, f)

with open(encoder_path, "wb") as f:
    pickle.dump(label_encoder, f)

print(f"\nModel saved to: {model_path}")
print(f"Label encoder saved to: {encoder_path}")
print("\nTraining complete! You can now run app.py to start the web server.")
