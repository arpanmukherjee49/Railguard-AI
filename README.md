# 🚂 RailGuard AI

**IoT + Machine Learning Based Predictive Maintenance of Electric Train Traction-Motor Bearings**

RailGuard AI is a hackathon prototype that monitors traction-motor operating parameters and classifies bearing condition as **Normal, Degrading, or Fault** using a Random Forest model.

> **Prototype note:** training data and dashboard values are synthetic/simulated. This is an educational prototype, not a validated railway safety or maintenance system.

## Architecture

```text
DHT22 ───────────────┐
MPU6050 ─────────────┤
Current simulation ──┤ → ESP32 → Wi-Fi → MQTT → Python → Random Forest → Condition
Load simulation ─────┘

Demo Dashboard:
Simulated Data → Random Forest → Streamlit Dashboard → Health / Alert / Trends
```

## Parameters

| Parameter | Prototype source | Purpose |
|---|---|---|
| Temperature | DHT22 | Thermal behaviour |
| Vibration-related acceleration | MPU6050 | Mechanical behaviour |
| Motor current | Potentiometer simulation | Electrical loading |
| Motor load | Potentiometer simulation | Operating condition |

## Machine Learning

Features: `Temperature`, `Vibration`, `Current`, `Load`.

Classes: `Normal`, `Degrading`, `Fault`.

The training script creates 3,000 synthetic prototype samples and saves `railguard_training_data.csv` and `railguard_model.pkl`. Model performance on this synthetic dataset must **not** be interpreted as real-world railway accuracy.

## Repository

```text
RailGuard_AI/
├── dashboard.py
├── mqtt_subscriber.py
├── simulate_sensor.py
├── railguard_ml.py
├── test_model.py
├── railguard_training_data.csv
├── railguard_model.pkl
├── requirements.txt
├── PROJECT_INFO.json
├── .gitignore
├── LICENSE
├── docs/
│   ├── architecture.md
│   └── demo-script.md
└── wokwi/
    ├── sketch.ino
    └── diagram.json
```

## Install

```bash
python -m pip install -r requirements.txt
```

## Train / regenerate model

```bash
python railguard_ml.py
```

## Test model

```bash
python test_model.py
```

## MQTT demo

Broker: `broker.hivemq.com`  
Port: `1883`  
Topic: `railguard/demo/traction_bearing`

Terminal 1:

```bash
python mqtt_subscriber.py
```

Terminal 2:

```bash
python simulate_sensor.py
```

The simulator cycles through Normal → Degrading → Fault every 60 seconds.

## Dashboard

The presentation dashboard deliberately runs independently of MQTT for reliability during the online demo:

```bash
python -m streamlit run dashboard.py
```

It is clearly labelled **DEMO MODE — Sensor values are simulated for prototype demonstration**.

## Wokwi

The `wokwi/` folder contains the ESP32 prototype setup. Pin mapping:

| Component | ESP32 |
|---|---|
| DHT22 DATA | GPIO 4 |
| MPU6050 SDA | GPIO 21 |
| MPU6050 SCL | GPIO 22 |
| Current potentiometer | GPIO 34 |
| Load potentiometer | GPIO 35 |
| Normal LED | GPIO 25 |
| Degrading LED | GPIO 26 |
| Fault LED | GPIO 27 |

The potentiometers simulate traction-motor parameters; a real implementation would use appropriate sensors.

## Technical note: vibration

The MPU6050 provides 3-axis acceleration. The prototype uses acceleration magnitude as a vibration-related parameter. Because an accelerometer also senses gravity, a production implementation should use suitable filtering/windowing and vibration-feature extraction.

## Future scope

Real labelled railway bearing data, robust vibration features, speed/load compensation, time-series anomaly detection, RUL estimation, fleet monitoring, maintenance-system integration, sensor redundancy, and railway-grade hardware/validation.

## License

MIT. See `LICENSE`.
