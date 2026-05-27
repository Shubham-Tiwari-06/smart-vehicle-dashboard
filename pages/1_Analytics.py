import streamlit as st
import pyrebase
import pandas as pd
import plotly.express as px

# =====================================================
# ================= PAGE CONFIG =======================
# =====================================================

st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide"
)

# =====================================================
# ================= FIREBASE ==========================
# =====================================================

firebaseConfig = {
    "apiKey": "AIzaSyDk7dKxXuuiH2drgXU4kfEPt3xeLouC7xw",
    "authDomain": "smartvehiclesafetysystem.firebaseapp.com",
    "databaseURL": "https://smartvehiclesafetysystem-default-rtdb.firebaseio.com",
    "storageBucket": "smartvehiclesafetysystem.appspot.com",
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

data = db.child("vehicle").get().val()

# =====================================================
# ================= TITLE =============================
# =====================================================

st.title("📈 Vehicle Analytics")

# =====================================================
# ================= DATAFRAME =========================
# =====================================================

df = pd.DataFrame({

    "Sensor": [
        "Acceleration",
        "MQ3",
        "Distance",
        "Speed",
        "LDR"
    ],

    "Value": [
        data["totalAccel"],
        data["mq3_raw"],
        data["distance_cm"],
        data["gpsSpeed"],
        data["ldrValue"]
    ]
})

st.dataframe(df, use_container_width=True)

# =====================================================
# ================= BAR CHART =========================
# =====================================================

fig = px.bar(
    df,
    x="Sensor",
    y="Value",
    title="Realtime Sensor Values"
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# ================= PIE CHART =========================
# =====================================================

status_data = pd.DataFrame({

    "Status": [
        "Accident",
        "Alcohol",
        "Obstacle"
    ],

    "Value": [
        int(data["accident"]),
        int(data["alcoholDetected"]),
        int(data["obstacleDetected"])
    ]
})

fig2 = px.pie(
    status_data,
    names="Status",
    values="Value",
    title="Alert Distribution"
)

st.plotly_chart(fig2, use_container_width=True)
