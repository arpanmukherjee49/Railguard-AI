"""RailGuard AI Streamlit demo dashboard. Uses clearly labelled simulated data."""
import time
import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="RailGuard AI", page_icon="🚂", layout="wide")
model = joblib.load("railguard_model.pkl")
st.title("🚂 RailGuard AI")
st.caption("IoT + Machine Learning Based Predictive Maintenance for Electric Train Traction-Motor Bearings")
st.warning("🟡 DEMO MODE — Sensor values are simulated for prototype demonstration")

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "history" not in st.session_state:
    st.session_state.history = []

elapsed = int(time.time() - st.session_state.start_time)
phase = elapsed % 60
if phase < 20:
    temperature, vibration, current, load = np.random.normal(42,1.2), np.random.normal(10.2,.6), np.random.normal(8.5,.5), np.random.normal(40,3)
elif phase < 40:
    p = (phase-20)/20
    temperature, vibration, current, load = 45+p*10+np.random.normal(0,1), 11+p*4+np.random.normal(0,.6), 10+p*5+np.random.normal(0,.5), 50+p*20+np.random.normal(0,3)
else:
    p = (phase-40)/20
    temperature, vibration, current, load = 56+p*15+np.random.normal(0,1.5), 15+p*7+np.random.normal(0,.8), 15+p*7+np.random.normal(0,.7), 70+p*20+np.random.normal(0,3)

temperature, vibration, current = max(20,temperature), max(0,vibration), max(0,current)
load = min(100,max(0,load))
reading = pd.DataFrame([{"Temperature":temperature,"Vibration":vibration,"Current":current,"Load":load}])
condition = model.predict(reading)[0]
probs = dict(zip(model.classes_, model.predict_proba(reading)[0]))
health = float(np.clip(probs.get("Normal",0)*100 + probs.get("Degrading",0)*55 + probs.get("Fault",0)*15,0,100))
state = condition.upper()
recommendation = {"NORMAL":"Continue normal operation and routine monitoring.","DEGRADING":"Early degradation detected. Schedule inspection during the next maintenance window.","FAULT":"Critical abnormal behaviour detected. Immediate maintenance inspection recommended."}[condition]

st.session_state.history.append({"Time":elapsed,"Temperature":temperature,"Vibration":vibration,"Current":current,"Load":load,"Health":health})
st.session_state.history = st.session_state.history[-60:]
df = pd.DataFrame(st.session_state.history)

c1,c2,c3,c4 = st.columns(4)
c1.metric("🌡️ Bearing Temperature",f"{temperature:.1f} °C")
c2.metric("📳 Vibration",f"{vibration:.2f} m/s²")
c3.metric("⚡ Motor Current",f"{current:.1f} A")
c4.metric("🚂 Motor Load",f"{load:.1f} %")
st.divider(); st.subheader("🤖 AI Bearing Condition")
if state == "NORMAL": st.success(f"🟢 NORMAL — Health Score: {health:.0f}%")
elif state == "DEGRADING": st.warning(f"🟡 DEGRADING — Health Score: {health:.0f}%")
else: st.error(f"🔴 FAULT — Health Score: {health:.0f}%")
st.info("🔧 Maintenance Recommendation: " + recommendation)

g1,g2 = st.columns(2)
with g1:
    fig=go.Figure(go.Indicator(mode="gauge+number",value=health,title={"text":"Bearing Health Score"},gauge={"axis":{"range":[0,100]},"threshold":{"line":{"width":4},"value":health}})); fig.update_layout(height=300); st.plotly_chart(fig,use_container_width=True)
with g2:
    st.markdown("### 📋 System Status"); st.write(f"**Operating State:** {state}"); st.write(f"**Temperature:** {temperature:.1f} °C"); st.write(f"**Vibration:** {vibration:.2f} m/s²"); st.write(f"**Motor Current:** {current:.1f} A"); st.write(f"**Motor Load:** {load:.1f} %")

st.divider(); st.subheader("📈 Live Sensor Trends")
if len(df)>1:
    fig=go.Figure(); fig.add_trace(go.Scatter(x=df.Time,y=df.Temperature,mode="lines",name="Temperature (°C)")); fig.add_trace(go.Scatter(x=df.Time,y=df.Vibration,mode="lines",name="Vibration (m/s²)")); fig.update_layout(xaxis_title="Time (s)",yaxis_title="Sensor Value",height=400,hovermode="x unified"); st.plotly_chart(fig,use_container_width=True)

x1,x2=st.columns(2)
with x1:
    fig=go.Figure(go.Scatter(x=df.Time,y=df.Current,mode="lines",name="Motor Current")); fig.update_layout(title="Motor Current",xaxis_title="Time (s)",yaxis_title="Current (A)",height=300); st.plotly_chart(fig,use_container_width=True)
with x2:
    fig=go.Figure(go.Scatter(x=df.Time,y=df.Load,mode="lines",name="Motor Load")); fig.update_layout(title="Motor Load",xaxis_title="Time (s)",yaxis_title="Load (%)",height=300); st.plotly_chart(fig,use_container_width=True)

st.divider(); st.caption("RailGuard AI Prototype | Simulated sensor data for demonstration. Real deployment would use actual traction-motor sensor measurements.")
time.sleep(1); st.rerun()
