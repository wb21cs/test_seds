import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry_convert as pc
import numpy as np

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


def get_continent_code(country_name):
    try:
        country_code = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        return continent_code
    except:
        return np.nan


df = pd.read_csv("data/medals.csv")
df["continent"] = df["country_code"].apply(get_continent_code)
df.loc[df["country_code"] == "KOS", "continent"] = "EU"
df["continent"] = df["continent"].fillna("Other")

# df

fig = px.sunburst(df, path=['continent', 'country_code', 'discipline'], color="continent", title = "Distribution Of Medals By Continent, Country and Discipline")
st.plotly_chart(fig)