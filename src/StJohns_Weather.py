""" 
    Streamlit front-end
    Author: Jillian Ivie
"""

import streamlit as st
import pandas as pd #data manipulation and creating DataFrames
import altair as alt #create interactive charts
from data import reload_data, last_updated
import requests

st.set_page_config(
    page_title= "Saint Johns Weather",
    
)

#inject custom CSS to hide the default header
st.markdown(
    """
    <style>
        header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


# Step 1: Fetch point metadata
POINTS_URL = "https://api.weather.gov/points/34.6164,-109.422"
points_response = requests.get(POINTS_URL, timeout = 3)
points_data = points_response.json()

# Step 2: Get the forecast URL from metadata
forecast_url = points_data["properties"]["forecast"]

# Step 3: Fetch the actual forecast data
forecast_response = requests.get(forecast_url, timeout=3)
forecast = forecast_response.json()

#retrieve weather forecast data from API
if "properties" in forecast and "periods" in forecast["properties"]:
    periods = forecast["properties"]["periods"]
    #process wind speed values
    for p in periods:
        p["wind"] = max([int(w) for w in p["windSpeed"].split() if w.isdigit()])
else:
    print("Error: 'properties' or 'periods' key not found in forecast data.")
    



#display title and last updated information
st.title("Weather Forecast")
st.header("for Saint Johns, AZ") 
st.subheader(f"Updated: {last_updated(forecast)}")

#create a container for Metrics
with st.container(border=True): #create container block with a border
    col1, col2, col3 = st.columns(3) #split container into three equal width columns
    col1.metric("Temperature", f"{periods[0]['temperature']} °F")
    col2.metric("Wind", f"{periods[0]['windSpeed']}")
    col3.metric("Rain Chance", f"{periods[0]['probabilityOfPrecipitation']['value']} %")
    
#create sidebar update button
update_bin = st.sidebar.button("Update", type="primary", on_click=reload_data)

#prepare data for visualization
columns = ["isDaytime", "temperature", "name", "wind", "shortForecast"] #define subset of keys from each period relevant to chart
chart_data = pd.DataFrame(periods, columns=columns)

#create altair chart
c = (
    alt.Chart(chart_data) #altair chart object using DataFrame
    .mark_circle() #represent data points as circles
    .encode(
        x=alt.X("name", sort=None, title="Day"), #name field for x axis
        y=alt.Y("temperature", title="Temperature (F)"), #temperature field for y axis
        size=alt.Size("wind", title="Wind Speed (mph)"), #circle size based on wind value
        color=alt.Color("isDaytime", legend=None).scale(scheme="blueorange"), #color circles based on daytime
        tooltip=alt.Tooltip("shortForecast"), #show shortForecast when hovering over data point
    )
)

#display chart
st.altair_chart(c, use_container_width=True, theme=None)