""" Streamlit front-end for api.weather.gov """
import streamlit as st
from requests import get


forecast = get(
    "https://api.weather.gov/points/34.6164,-109.422", timeout=3).json()
st.title("Weather Forecast")
st.table(forecast.get("properties").get("periods"))
