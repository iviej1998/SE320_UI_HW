""" 
    Streamlit front-end (Table View) for api.weather.gov 
    Author: Jillian Ivie
"""
import streamlit as st
from data import reload_data, fetch_data, last_updated

forecast = fetch_data(DATA_URL = "https://api.weather.gov/gridpoints/FGZ/152,54/forecast", DATA_FILE = "./app/data/weather.json")
periods = forecast.get("properties").get("periods")

st.title("Weather Data Table")
st.subheader(f"Updated: {last_updated(forecast)}")

update_btn = st.sidebar.button("Update", type="primary", on_click=reload_data)
day_time_only = st.sidebar.toggle("Only show daytime temperatures", value=True)
columns = st.sidebar.multiselect("Select the columns to be displayed:", list(
    periods[0].keys()), default=["name", "temperature"], placeholder="Select columns")
custom = [{k: v for k, v in p.items() if k in columns}
        for p in periods if p["isDaytime"] or not day_time_only]
st.table(custom)
