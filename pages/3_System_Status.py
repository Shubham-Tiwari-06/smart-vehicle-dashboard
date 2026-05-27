import streamlit as st
import pyrebase

st.set_page_config(
    page_title="System Status",
    page_icon="⚙",
    layout="wide"
)

firebaseConfig = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "smartvehiclesafetysystem.firebaseapp.com",
    "databaseURL": "https://smartvehiclesafetysystem-default-rtdb.firebaseio.com",
    "storageBucket": "smartvehiclesafetysystem.appspot.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

data = db.child("vehicle").get().val()

st.title("⚙ System Status")

# =====================================================
# ================= SENSOR STATUS =====================
# =====================================================

sensor_status = {

    "MPU6050": "ONLINE",
    "MQ3": "ONLINE",
    "Ultrasonic": "ONLINE",
    "GPS": "ONLINE",
    "LCD": "ONLINE",
    "WiFi": "CONNECTED"
}

for sensor, status in sensor_status.items():

    st.success(f"{sensor} : {status}")

# =====================================================
# ================= ALERTS ============================
# =====================================================

if data["accident"]:
    st.error("ACCIDENT DETECTED")

if data["alcoholDetected"]:
    st.warning("ALCOHOL DETECTED")

if data["obstacleDetected"]:
    st.warning("OBSTACLE DETECTED")