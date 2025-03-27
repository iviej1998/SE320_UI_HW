""" Streamlit front-end for api.weather.gov """
import streamlit as st
from requests import get


forecast = get(
    "https://api.weather.gov/gridpoints/FGZ/185,76/forecast", timeout=3).json()
periods = forecast.get("properties").get("periods")
keys = ["startTime", "temperature", "isDaytime"]
concise = [{k: v for k, v in p.items() if k in keys} for p in periods]
st.title("Weather Forecast")
st.table(concise)
