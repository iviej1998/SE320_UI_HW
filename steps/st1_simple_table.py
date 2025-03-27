""" Streamlit front-end """
import streamlit as st
from requests import get


forecast = get(
    "https://api.weather.gov/points/36.4216,-109.4842", timeout=3).json()
st.title("Weather Forecast")
st.table(forecast.get("properties").get("periods"))
