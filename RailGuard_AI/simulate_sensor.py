"""Publish simulated Normal -> Degrading -> Fault sensor data over MQTT."""
import json
import random
import time
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "railguard/demo/traction_bearing"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT, 60)
print("Connected to MQTT broker")
print("Publishing to:", TOPIC)
start = time.time()

try:
    while True:
        elapsed = int(time.time() - start)
        phase = elapsed % 60
        if phase < 20:
            state = "NORMAL"
            temperature, vibration, current, load = random.gauss(40,1.5), random.gauss(10,.7), random.gauss(8,.5), random.gauss(40,3)
        elif phase < 40:
            state = "DEGRADING"
            progress = (phase-20)/20
            temperature, vibration, current, load = 45+progress*10+random.gauss(0,.8), 11+progress*4+random.gauss(0,.5), 10+progress*5+random.gauss(0,.4), 50+progress*20+random.gauss(0,2)
        else:
            state = "FAULT"
            progress = (phase-40)/20
            temperature, vibration, current, load = 56+progress*15+random.gauss(0,1), 15+progress*7+random.gauss(0,.7), 15+progress*7+random.gauss(0,.5), 70+progress*20+random.gauss(0,2)
        payload = {"temperature": round(max(0,temperature),2), "vibration": round(max(0,vibration),2), "current": round(max(0,current),2), "load": round(min(100,max(0,load)),2)}
        client.publish(TOPIC, json.dumps(payload))
        print(f"[{elapsed:03d}s] {state:10s} | T={payload['temperature']:.1f}°C | V={payload['vibration']:.2f} | I={payload['current']:.1f}A | Load={payload['load']:.1f}%")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSensor simulator stopped.")
finally:
    client.disconnect()
