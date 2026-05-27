import streamlit as st
import pyrebase
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# =====================================================
# ================= PAGE CONFIG =======================
# =====================================================

st.set_page_config(page_title="Smart Vehicle Dashboard", page_icon="🚗", layout="wide")

# =====================================================
# ================= AUTO REFRESH ======================
# =====================================================

st_autorefresh(interval=2000, key="refresh")

# =====================================================
# ================= CUSTOM CSS ========================
# =====================================================

st.markdown(
    """
<style>

[data-testid="stAppViewContainer"] {
    background-color: #0f172a;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3 {
    color: white;
}

</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# ================= FIREBASE CONFIG ===================
# =====================================================

firebaseConfig = {
    "apiKey": "AIzaSyDk7dKxXuuiH2drgXU4kfEPt3xeLouC7xw",
    "authDomain": "smartvehiclesafetysystem.firebaseapp.com",
    "databaseURL": "https://smartvehiclesafetysystem-default-rtdb.firebaseio.com",
    "storageBucket": "smartvehiclesafetysystem.appspot.com",
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

# =====================================================
# ================= FETCH DATA ========================
# =====================================================

data = db.child("vehicle").get().val()

if data is None:
    st.error("No Firebase Data Found")
    st.stop()

# =====================================================
# ================= SESSION STORAGE ===================
# =====================================================

if "time_data" not in st.session_state:

    st.session_state.time_data = []

    st.session_state.accel_data = []

    st.session_state.mq3_data = []

    st.session_state.distance_data = []

    st.session_state.speed_data = []

# =====================================================
# ================= STORE VALUES ======================
# =====================================================

current_time = datetime.now().strftime("%H:%M:%S")

st.session_state.time_data.append(current_time)

st.session_state.accel_data.append(data["totalAccel"])

st.session_state.mq3_data.append(data["mq3_raw"])

st.session_state.distance_data.append(data["distance_cm"])

st.session_state.speed_data.append(data["gpsSpeed"])

# =====================================================
# ================= KEEP LAST 20 VALUES ===============
# =====================================================

MAX_POINTS = 20

if len(st.session_state.time_data) > MAX_POINTS:

    st.session_state.time_data.pop(0)

    st.session_state.accel_data.pop(0)

    st.session_state.mq3_data.pop(0)

    st.session_state.distance_data.pop(0)

    st.session_state.speed_data.pop(0)

# =====================================================
# ================= SIDEBAR ===========================
# =====================================================

st.sidebar.title("🚗 Smart Vehicle System")

st.sidebar.success("ESP32 Connected")

st.sidebar.write("Realtime IoT Monitoring")

# =====================================================
# ================= TITLE =============================
# =====================================================

st.title("🚗 Smart Vehicle Safety Dashboard")

st.markdown("---")

# =====================================================
# ================= ALERTS ============================
# =====================================================

if data["accident"]:
    st.error("⚠️ ACCIDENT DETECTED")

if data["alcoholDetected"]:
    st.warning("🍺 Alcohol Detected")

if data["obstacleDetected"]:
    st.warning("🚧 Obstacle Detected")

# =====================================================
# ================= TOP METRICS =======================
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Acceleration", f'{data["totalAccel"]} g')

with col2:
    st.metric("MQ3", data["mq3_raw"])

with col3:
    st.metric("Distance", f'{data["distance_cm"]} cm')

with col4:
    st.metric("Speed", f'{data["gpsSpeed"]} km/h')

# =====================================================
# ================= MPU6050 DATA ======================
# =====================================================

st.subheader("📡 MPU6050 Sensor")

col5, col6, col7 = st.columns(3)

with col5:
    st.metric("Acc X", data["accX"])
    st.metric("Gyro X", data["gyroX"])

with col6:
    st.metric("Acc Y", data["accY"])
    st.metric("Gyro Y", data["gyroY"])

with col7:
    st.metric("Acc Z", data["accZ"])
    st.metric("Gyro Z", data["gyroZ"])

# =====================================================
# ================= VEHICLE STATUS ====================
# =====================================================

st.subheader("🚘 Vehicle Status")

col8, col9, col10 = st.columns(3)

with col8:

    headlight = "HIGH BEAM" if data["highBeam"] else "LOW BEAM"

    st.success(headlight)

with col9:

    if data["alcoholDetected"]:
        st.error("ALCOHOL DETECTED")
    else:
        st.success("NO ALCOHOL")

with col10:

    if data["obstacleDetected"]:
        st.error("OBSTACLE DETECTED")
    else:
        st.success("ROAD CLEAR")

# =====================================================
# ================= SMART HEADLIGHT ===================
# =====================================================

st.subheader("💡 Smart Headlight")

col11, col12 = st.columns(2)

with col11:
    st.metric("LDR Value", data["ldrValue"])

with col12:
    st.metric("LED Brightness", data["ledBrightness"])

# =====================================================
# ================= GPS SECTION =======================
# =====================================================

st.subheader("🛰 GPS Location")

col13, col14 = st.columns(2)

with col13:
    st.metric("Latitude", data["latitude"])

with col14:
    st.metric("Longitude", data["longitude"])

# =====================================================
# ================= MAP ===============================
# =====================================================

map_data = pd.DataFrame({"lat": [data["latitude"]], "lon": [data["longitude"]]})

st.map(map_data)

# =====================================================
# ================= GAUGE METERS ======================
# =====================================================

st.subheader("📊 Live Gauge Monitoring")

g1, g2 = st.columns(2)

# ================= SPEED GAUGE =================

with g1:

    fig_speed = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=data["gpsSpeed"],
            title={"text": "Vehicle Speed (km/h)"},
            gauge={
                "axis": {"range": [0, 120]},
                "bar": {"color": "green"},
                "steps": [
                    {"range": [0, 40], "color": "lightgreen"},
                    {"range": [40, 80], "color": "yellow"},
                    {"range": [80, 120], "color": "red"},
                ],
            },
        )
    )

    st.plotly_chart(fig_speed, use_container_width=True)

# ================= ACCELERATION GAUGE =================

with g2:

    fig_accel = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=data["totalAccel"],
            title={"text": "Acceleration (g)"},
            gauge={
                "axis": {"range": [0, 5]},
                "bar": {"color": "blue"},
                "steps": [
                    {"range": [0, 1.5], "color": "lightgreen"},
                    {"range": [1.5, 2.5], "color": "yellow"},
                    {"range": [2.5, 5], "color": "red"},
                ],
            },
        )
    )

    st.plotly_chart(fig_accel, use_container_width=True)

# ================= SECOND ROW =================

g3, g4 = st.columns(2)

# ================= MQ3 GAUGE =================

with g3:

    fig_mq3 = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=data["mq3_raw"],
            title={"text": "MQ3 Alcohol Level"},
            gauge={
                "axis": {"range": [0, 4095]},
                "bar": {"color": "orange"},
                "steps": [
                    {"range": [0, 1500], "color": "lightgreen"},
                    {"range": [1500, 2500], "color": "yellow"},
                    {"range": [2500, 4095], "color": "red"},
                ],
            },
        )
    )

    st.plotly_chart(fig_mq3, use_container_width=True)

# ================= DISTANCE GAUGE =================

with g4:

    fig_distance = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=data["distance_cm"],
            title={"text": "Obstacle Distance (cm)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "purple"},
                "steps": [
                    {"range": [0, 20], "color": "red"},
                    {"range": [20, 50], "color": "yellow"},
                    {"range": [50, 100], "color": "lightgreen"},
                ],
            },
        )
    )

    st.plotly_chart(fig_distance, use_container_width=True)


# =====================================================
# ================= SMART ANALYTICS ===================
# =====================================================

st.subheader("🧠 Smart Vehicle Analytics")

# ================= SAFETY SCORE =================

safety_score = 100

if data["accident"]:
    safety_score -= 50

if data["alcoholDetected"]:
    safety_score -= 25

if data["obstacleDetected"]:
    safety_score -= 15

if data["gpsSpeed"] > 80:
    safety_score -= 10

if data["totalAccel"] > 2:
    safety_score -= 10

safety_score = max(safety_score, 0)

# ================= ROAD CONDITION =================

road_condition = "Smooth Road"

if data["totalAccel"] > 1.4:
    road_condition = "Rough Road"

if data["totalAccel"] > 2:
    road_condition = "Possible Pothole"

# ================= DISPLAY =================

a1, a2, a3 = st.columns(3)

# ================= SAFETY SCORE =================

with a1:

    st.metric("Driver Safety Score", f"{safety_score}/100")

    st.progress(safety_score / 100)

# ================= ROAD CONDITION =================

with a2:

    if road_condition == "Smooth Road":
        st.success(road_condition)

    elif road_condition == "Rough Road":
        st.warning(road_condition)

    else:
        st.error(road_condition)

# ================= SYSTEM HEALTH =================

with a3:

    system_health = "GOOD"

    if data["accident"] or data["alcoholDetected"]:
        system_health = "CRITICAL"

    elif data["obstacleDetected"]:
        system_health = "WARNING"

    if system_health == "GOOD":
        st.success("System Healthy")

    elif system_health == "WARNING":
        st.warning("System Warning")

    else:
        st.error("Critical Condition")

# =====================================================
# ================= SENSOR BARS =======================
# =====================================================

st.subheader("📊 Sensor Intensity")

b1, b2 = st.columns(2)

# ================= MQ3 LEVEL =================

with b1:

    st.write("Alcohol Sensor Level")

    mq3_percent = min(data["mq3_raw"] / 4095, 1.0)

    st.progress(mq3_percent)

    st.write(f"{round(mq3_percent * 100, 1)} %")

# ================= ACCELERATION LEVEL =================

with b2:

    st.write("Acceleration Severity")

    accel_percent = min(data["totalAccel"] / 5, 1.0)

    st.progress(accel_percent)

    st.write(f"{round(accel_percent * 100, 1)} %")

# =====================================================
# ================= LIVE SENSOR GRAPHS ================
# =====================================================

st.subheader("📈 Live Sensor Graphs")

# ================= ACCELERATION GRAPH =================

accel_df = pd.DataFrame(
    {"Time": st.session_state.time_data, "Acceleration": st.session_state.accel_data}
)

fig1 = px.line(accel_df, x="Time", y="Acceleration", title="Total Acceleration")

st.plotly_chart(fig1, use_container_width=True)

# ================= MQ3 GRAPH =================

mq3_df = pd.DataFrame(
    {"Time": st.session_state.time_data, "MQ3": st.session_state.mq3_data}
)

fig2 = px.line(mq3_df, x="Time", y="MQ3", title="MQ3 Alcohol Sensor")

st.plotly_chart(fig2, use_container_width=True)

# ================= DISTANCE GRAPH =================

distance_df = pd.DataFrame(
    {"Time": st.session_state.time_data, "Distance": st.session_state.distance_data}
)

fig3 = px.line(distance_df, x="Time", y="Distance", title="Ultrasonic Distance")

st.plotly_chart(fig3, use_container_width=True)

# ================= SPEED GRAPH =================

speed_df = pd.DataFrame(
    {"Time": st.session_state.time_data, "Speed": st.session_state.speed_data}
)

fig4 = px.line(speed_df, x="Time", y="Speed", title="GPS Speed")

st.plotly_chart(fig4, use_container_width=True)

# =====================================================
# ================= RAW FIREBASE DATA =================
# =====================================================

with st.expander("Show Raw Firebase Data"):
    st.json(data)
