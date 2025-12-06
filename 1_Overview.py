import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Overview")

nb_athletes = pd.read_csv("data/athletes.csv")["code"].count()
nb_countries = pd.read_csv("data/nocs.csv")["code"].count()
nb_sports = pd.read_csv("data/events.csv")["sport_code"].nunique()
total_medals = pd.read_csv("data/medals_total.csv")["Total"].sum()
nb_events = pd.read_csv("data/events.csv")["event"].count()

# Metrics
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Athletes", nb_athletes)
col2.metric("Countries", nb_countries)
col3.metric("Sports", nb_sports)
col4.metric("Medals Awarded", total_medals)
col5.metric("Events", nb_events)




medal_df = pd.read_csv("data/medals_total.csv")

medal_counts = medal_df[['Gold', 'Silver', 'Bronze']].sum().reset_index()
medal_counts.columns = ['Medal', 'Count']


fig = px.bar(medal_counts, x="Medal", y="Count", color="Medal", title="Global Medal Distribution")

st.plotly_chart(fig)