# RailGuard AI Architecture

**Sense → Communicate → Analyse → Predict → Act**

1. **Sensing:** temperature, vibration-related acceleration, motor current and load.
2. **IoT:** ESP32 collects readings and provides Wi-Fi connectivity.
3. **Communication:** MQTT carries JSON sensor messages.
4. **Analytics:** Python loads the trained Random Forest classifier.
5. **Decision:** Normal / Degrading / Fault.
6. **Visualization:** Streamlit displays health, trends and maintenance guidance.

MQTT topic: `railguard/demo/traction_bearing`
