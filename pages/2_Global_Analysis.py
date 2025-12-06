import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry_convert as pc
import numpy as np

st.title("Global Analysis")

# --------------------------------------
# LOAD BASE DATA
# --------------------------------------
raw_df = pd.read_csv("data/medals_total.csv")
map_df = raw_df.loc[:, ["country_code", "country", "Total"]]


# --------------------------------------
# Helper: Get continent
# --------------------------------------
def get_continent_code(country_name):
    try:
        country_code = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        return continent_code
    except:
        return np.nan


# Add continent column
raw_df["continent"] = raw_df["country_code"].apply(get_continent_code)
raw_df.loc[raw_df["country_code"] == "XKX", "continent"] = "EU"
raw_df["continent"] = raw_df["continent"].fillna("Other")


# --------------------------------------
# SIDEBAR FILTERS (EMPTY BY DEFAULT)
# --------------------------------------
continent_list = sorted(raw_df["continent"].unique())
country_list = sorted(raw_df["country"].unique())
medal_list = ["Gold", "Silver", "Bronze"]

st.sidebar.title("Filters")

selected_continent = st.sidebar.multiselect("Select Continent(s)", continent_list)
selected_countries = st.sidebar.multiselect("Select Country/Countries", country_list)
selected_medals = st.sidebar.multiselect("Select Medals", medal_list)

# --------------------------------------
# APPLY FILTERS SAFELY
# --------------------------------------
filtered_df = raw_df.copy()

# continent
if selected_continent:
    filtered_df = filtered_df[filtered_df["continent"].isin(selected_continent)]

# countries
if selected_countries:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

# --------------------------------------
# WORLD MAP (Filtered)
# --------------------------------------
map_display = filtered_df.loc[:, ["country_code", "country", "Total"]]

fig = px.choropleth(
    map_display,
    locations="country_code",
    color="Total",
    hover_name="country",
    color_continuous_scale="Viridis",
    title="Total Medals per Country"
)
st.plotly_chart(fig, use_container_width=True)


# --------------------------------------
# MEDALS BY CONTINENT (Filtered + Optional Medal Filter)
# --------------------------------------
medal_df = filtered_df.copy()

# melt medals
if selected_medals:
    medal_df = medal_df.melt(
        id_vars=["country", "continent"],
        value_vars=selected_medals,
        var_name="medal",
        value_name="count"
    )
else:
    medal_df = medal_df.melt(
        id_vars=["country", "continent"],
        value_vars=medal_list,
        var_name="medal",
        value_name="count"
    )

# group
grouped = medal_df.groupby(["continent", "medal"], as_index=False)["count"].sum()

fig = px.bar(grouped, x="continent", y="count", color="medal",
             title="Medals by Continent (Filtered)")
st.plotly_chart(fig)


# --------------------------------------
# SUNBURST (Filtered)
# --------------------------------------
sunburst_df = pd.read_csv("data/medals.csv")
sunburst_df["continent"] = sunburst_df["country_code"].apply(get_continent_code)
sunburst_df.loc[sunburst_df["country_code"] == "KOS", "continent"] = "EU"
sunburst_df["continent"] = sunburst_df["continent"].fillna("Other")

# apply same continent/country filters
if selected_continent:
    sunburst_df = sunburst_df[sunburst_df["continent"].isin(selected_continent)]
if selected_countries:
    sunburst_df = sunburst_df[sunburst_df["country"].isin(selected_countries)]

fig = px.sunburst(
    sunburst_df,
    path=["continent", "country_code", "discipline"],
    color="continent",
    title="Distribution Of Medals By Continent, Country and Discipline (Filtered)"
)
st.plotly_chart(fig)


# --------------------------------------
# TOP 20 RANKING (Filtered + Medal Filter)
# --------------------------------------
ranking_df = filtered_df.copy()

ranking_df = ranking_df.sort_values(
    by=["Gold", "Silver", "Bronze"],
    ascending=[False, False, False]
).head(20)

# Use selected medals if any, otherwise default to all
medals_to_use = selected_medals if selected_medals else ["Gold", "Silver", "Bronze"]

ranking_df = ranking_df.melt(
    id_vars=["country_code", "country"],
    value_vars=medals_to_use,
    var_name="medal",
    value_name="count"
)

fig = px.bar(
    ranking_df,
    x="country",
    y="count",
    color="medal",
    barmode="group",
    title="Top 20 Countries by Medals (Filtered)"
)
st.plotly_chart(fig)

