""" Streamlit front-end for api.weather.gov """
import streamlit as st
from requests import get


forecast = get(
"https://api.weather.gov/points/36.4216,-109.4842", timeout=3).json()
periods = forecast.get("properties").get("periods")
all_cols = list(periods[0].keys())

st.title("Weather Forecast")
columns = st.multiselect(
    "Select the columns to be displayed:", all_cols, placeholder="Select columns")
custom = [{k: v for k, v in p.items() if k in columns} for p in periods]
st.table(custom)
