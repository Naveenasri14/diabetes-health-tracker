import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
data = pd.read_csv("diabetes_dataset.csv", sep=r"\s+")

print("Columns in dataset:")
print(data.columns)

# Replace invalid zeros
cols = ['Glucose','BloodPressure','SkinThickness','Insulin','BMI']
data[cols] = data[cols].replace(0, np.nan)

# Fill missing values
data.fillna(data.mean(), inplace=True)

print("\nFirst 5 rows of dataset:")
print(data.head())

# Features and target
X = data.drop("Outcome", axis=1)
y = data["Outcome"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTraining data shape:", X_train.shape)
print("Testing data shape:", X_test.shape)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
print("\nModel Accuracy:", accuracy)

# Save model
joblib.dump(model, "diabetes_model.pkl")

print("\nModel saved successfully!")