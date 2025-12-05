import streamlit as st
import pandas as pd
import plotly.express as px


st.title("Medailsts")

medal_df = pd.read_csv("data/medals_total.csv")

medal_counts = medal_df[['Gold', 'Silver', 'Bronze']].sum().reset_index()
medal_counts.columns = ['Medal', 'Count']


fig = px.bar(medal_counts, x="Medal", y="Count", color="Medal", title="Global Medal Distribution")

st.plotly_chart(fig)