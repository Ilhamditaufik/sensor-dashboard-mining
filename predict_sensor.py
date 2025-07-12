import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Load dataset
data = pd.read_csv("sensor_data.csv")

# Features dan label
X = data[["getaran", "suhu", "tekanan", "kelembapan"]]
y = data["status"]

# Encode label
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y_encoded)

# Save model dan label encoder
joblib.dump(clf, "model_sensor.pkl")
joblib.dump(le, "label_encoder.pkl")

print("✅ Model dan label encoder berhasil disimpan.")
