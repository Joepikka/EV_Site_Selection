import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# Load the MCDA-scored dataset
data = pd.read_csv("data/ev_sites_scored.csv")


# Features used to train the model
FEATURES = [
    "road_distance",
    "population_density",
    "existing_charger_distance",
    "slope",
    "flood_hazard",
    "commercial_score"
]


# X = input features
X = data[FEATURES]


# y = value the model tries to predict
y = data["suitability_class"]


# Split dataset:
# 80% for training
# 20% for testing

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Create Random Forest model

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    random_state=42,
    class_weight="balanced"
)


# Train the model

model.fit(X_train, y_train)


# Make predictions on test data

predictions = model.predict(X_test)


# Evaluate model

accuracy = accuracy_score(
    y_test,
    predictions
)


print("Model Accuracy:", accuracy)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)


# Create models folder if needed

os.makedirs(
    "models",
    exist_ok=True
)


# Save trained model

joblib.dump(
    model,
    "models/ev_random_forest.pkl"
)


print("\nModel saved successfully!")