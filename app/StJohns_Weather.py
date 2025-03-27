""" Module docstring """

import streamlit as st
from data import reload_data, fetch_data, last_updated

forecast = fetch_data()
