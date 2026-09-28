"""Receive MQTT sensor JSON and run the trained ML model."""
import json
import joblib
import pandas as pd
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "railguard/demo/traction_bearing"
model = joblib.load("railguard_model.pkl")


def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected to MQTT broker")
        client.subscribe(TOPIC)
        print("Subscribed to:", TOPIC)
    else:
        print("MQTT connection failed:", reason_code)


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        row = pd.DataFrame([{
            "Temperature": float(payload["temperature"]),
            "Vibration": float(payload["vibration"]),
            "Current": float(payload["current"]),
            "Load": float(payload["load"]),
        }])
        prediction = model.predict(row)[0]
        print("\n--- RailGuard Sensor Reading ---")
        print(f"Temperature : {row.iloc[0]['Temperature']:.2f} °C")
        print(f"Vibration   : {row.iloc[0]['Vibration']:.2f} m/s²")
        print(f"Current     : {row.iloc[0]['Current']:.2f} A")
        print(f"Load        : {row.iloc[0]['Load']:.2f} %")
        print("AI Diagnosis:", prediction)
    except (KeyError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print("Invalid MQTT payload:", exc)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
print(f"Connecting to {BROKER}:{PORT}...")
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nSubscriber stopped.")
