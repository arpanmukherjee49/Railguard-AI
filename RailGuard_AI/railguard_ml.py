"""Train the RailGuard AI Random Forest model on synthetic prototype data."""
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

RANDOM_STATE = 42
N_PER_CLASS = 1000
rng = np.random.default_rng(RANDOM_STATE)


def make_class_data(label, n):
    if label == "Normal":
        vals = [rng.normal(40, 3, n), rng.normal(10, 1.2, n), rng.normal(8, 1.2, n), rng.normal(40, 8, n)]
    elif label == "Degrading":
        vals = [rng.normal(50, 4, n), rng.normal(14, 1.8, n), rng.normal(13, 1.8, n), rng.normal(62, 9, n)]
    else:
        vals = [rng.normal(64, 5, n), rng.normal(20, 2.5, n), rng.normal(18, 2.2, n), rng.normal(82, 8, n)]
    return pd.DataFrame(dict(zip(["Temperature", "Vibration", "Current", "Load"], vals))).assign(Condition=label)


def main():
    data = pd.concat([make_class_data("Normal", N_PER_CLASS), make_class_data("Degrading", N_PER_CLASS), make_class_data("Fault", N_PER_CLASS)], ignore_index=True)
    data.to_csv("railguard_training_data.csv", index=False)
    features = ["Temperature", "Vibration", "Current", "Load"]
    model = RandomForestClassifier(n_estimators=150, random_state=RANDOM_STATE, class_weight="balanced", n_jobs=-1)
    model.fit(data[features], data["Condition"])
    joblib.dump(model, "railguard_model.pkl")
    print("Training complete. Created railguard_training_data.csv and railguard_model.pkl")


if __name__ == "__main__":
    main()
