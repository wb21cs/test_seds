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


medal_ranking_df = pd.read_csv("data/medals_total.csv").sort_values(
        by=["Gold", "Silver", "Bronze"],
        ascending=[False, False, False]
    ).loc[:, ["country_code", "country", "Gold", "Silver", "Bronze"]].head(20).melt(
        id_vars=["country_code", "country"],
        value_vars=['Gold', 'Silver', 'Bronze'],
        var_name='medal',
        value_name='count'
    )
medal_ranking_fig = px.bar(medal_ranking_df, x="country", y="count", color="medal", barmode="group", title="Country Ranking By Medals")
st.plotly_chart(medal_ranking_fig)