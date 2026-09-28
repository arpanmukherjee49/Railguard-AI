"""Quick test for the saved RailGuard AI model."""
import joblib
import pandas as pd

model = joblib.load("railguard_model.pkl")
reading = pd.DataFrame([{"Temperature": 39.0, "Vibration": 13.81, "Current": 15.0, "Load": 20.0}])
prediction = model.predict(reading)[0]
probabilities = model.predict_proba(reading)[0]
print("RailGuard AI Model Test")
print("Prediction:", prediction)
for cls, p in zip(model.classes_, probabilities):
    print(f"{cls}: {p*100:.2f}%")
