""" Streamlit front-end for api.weather.gov """
import streamlit as st
from requests import get


forecast = get(
    "https://api.weather.gov/points/34.6164,-109.422", timeout=3).json()
periods = forecast.get("properties").get("periods")
keys = ["startTime", "temperature", "isDaytime"]
concise = [{k: v for k, v in p.items() if k in keys} for p in periods]
st.title("Weather Forecast")
st.table(concise)
