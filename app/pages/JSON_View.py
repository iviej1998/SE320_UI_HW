""" 
    Streamlit front-end (JSON View) for api.weather.gov 
    Author: Jillian Ivie
"""
import streamlit as st
from data import fetch_data, last_updated, DATA_FILE

forecast = fetch_data(DATA_URL = "https://api.weather.gov/gridpoints/FGZ/185,76/forecast", DATA_FILE = "./app/data/weather.json")

st.title("Weather Data")
st.subheader(f"Updated: {last_updated(forecast)}")
st.json(forecast)
with open(DATA_FILE, encoding="utf-8") as f:
    st.sidebar.download_button(
        "Download JSON", f, file_name="stjohns_weather.json", mime="application/json", type="primary")
