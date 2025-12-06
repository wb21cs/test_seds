import streamlit as st
import pandas as pd
import plotly.express as px


st.title("Global Analysis")


map_df = pd.read_csv("data/medals_total.csv").loc[:, ["country_code", "country", "Total"]]

fig = px.choropleth(
    map_df,
    locations="country_code",        # or 'country_long' if using full names
    color="Total",          # Total medals
    hover_name="country",       # Shows country code on hover
    color_continuous_scale="Viridis",
    title="Total Medals per Country"
)

st.plotly_chart(fig, use_container_width=True)