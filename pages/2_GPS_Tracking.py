import streamlit as st
import pyrebase
import pandas as pd

st.set_page_config(
    page_title="GPS Tracking",
    page_icon="🛰",
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

st.title("🛰 Live GPS Tracking")

st.metric("Latitude", data["latitude"])

st.metric("Longitude", data["longitude"])

st.metric("Speed", f'{data["gpsSpeed"]} km/h')

map_data = pd.DataFrame({
    'lat': [data["latitude"]],
    'lon': [data["longitude"]]
})

st.map(map_data)