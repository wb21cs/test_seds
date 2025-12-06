import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry_convert as pc
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Global Analysis - Paris 2024",
    page_icon="🗺️",
    layout="wide"
)

# Load data once
@st.cache_data
def load_all_data():
    medals_total = pd.read_csv("data/medals_total.csv")
    medals = pd.read_csv("data/medals.csv")
    nocs = pd.read_csv("data/nocs.csv")
    events = pd.read_csv("data/events.csv")
    return medals_total, medals, nocs, events

medals_total_original, medals_original, nocs, events = load_all_data()

# SIDEBAR FILTERS
st.sidebar.header("🎯 Global Filters")

# Country filter
countries = sorted(nocs['country'].dropna().unique())
selected_countries = st.sidebar.multiselect(
    "🌍 Select Countries",
    countries,
    default=[],
    help="Filter data by specific countries"
)

# Sport filter
sports = sorted(events['sport'].dropna().unique())
selected_sports = st.sidebar.multiselect(
    "🏅 Select Sports",
    sports,
    default=[],
    help="Filter data by specific sports"
)

# Get continent function
def get_continent_code(country_code):
    try:
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        return continent_code
    except:
        return np.nan

def get_continent_name(continent_code):
    continent_mapping = {
        'AF': 'Africa',
        'AS': 'Asia',
        'EU': 'Europe',
        'NA': 'North America',
        'SA': 'South America',
        'OC': 'Oceania',
        np.nan: 'Other'
    }
    return continent_mapping.get(continent_code, 'Other')

# Add continent to medals_total
medals_total_original['continent_code'] = medals_total_original['country_code'].apply(get_continent_code)
medals_total_original.loc[medals_total_original['country_code'] == 'XKX', 'continent_code'] = 'EU'
medals_total_original['continent_name'] = medals_total_original['continent_code'].apply(get_continent_name)

# Continent filter (Creative Challenge!)
continents = sorted(medals_total_original['continent_name'].dropna().unique())
selected_continents = st.sidebar.multiselect(
    "🌏 Select Continents (Creative Filter!)",
    continents,
    default=[],
    help="Filter data by continent for regional analysis"
)

# Medal type filter
st.sidebar.subheader("🥇 Medal Types")
show_gold = st.sidebar.checkbox("Gold", value=True)
show_silver = st.sidebar.checkbox("Silver", value=True)
show_bronze = st.sidebar.checkbox("Bronze", value=True)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Use filters to customize your analysis!")

# Apply filters
medals_total_filtered = medals_total_original.copy()
medals_filtered = medals_original.copy()

# Filter by countries
if selected_countries:
    country_codes = nocs[nocs['country'].isin(selected_countries)]['code'].values
    medals_total_filtered = medals_total_filtered[medals_total_filtered['country_code'].isin(country_codes)]
    medals_filtered = medals_filtered[medals_filtered['country_code'].isin(country_codes)]

# Filter by continents
if selected_continents:
    medals_total_filtered = medals_total_filtered[medals_total_filtered['continent_name'].isin(selected_continents)]

# Filter by sports
if selected_sports:
    medals_filtered = medals_filtered[medals_filtered['discipline'].isin(selected_sports)]

# Filter by medal types
medal_columns = []
if show_gold:
    medal_columns.append('Gold')
if show_silver:
    medal_columns.append('Silver')
if show_bronze:
    medal_columns.append('Bronze')

if not medal_columns:
    medal_columns = ['Gold', 'Silver', 'Bronze']

# Filter medals by type
medal_type_map = {'Gold': 'Gold Medal', 'Silver': 'Silver Medal', 'Bronze': 'Bronze Medal'}
selected_medal_types = [medal_type_map[m] for m in medal_columns]
medals_filtered = medals_filtered[medals_filtered['medal_type'].isin(selected_medal_types)]

# Recalculate Total based on selected medal types
medals_total_filtered['Total'] = medals_total_filtered[medal_columns].sum(axis=1)

# Original code starts here
st.title("Global Analysis")

map_df = medals_total_filtered.loc[:, ["country_code", "country", "Total"]]

fig = px.choropleth(
    map_df,
    locations="country_code",        # or 'country_long' if using full names
    color="Total",          # Total medals
    hover_name="country",       # Shows country code on hover
    color_continuous_scale="Viridis",
    title="Total Medals per Country"
)

st.plotly_chart(fig, use_container_width=True)

def get_continent_code(country_name):
    try:
        country_code = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        return continent_code
    except:
        return np.nan

df = medals_total_filtered.copy()
df["continent"] = df["country_code"].apply(get_continent_code)
df.loc[df["country_code"] == "XKX", "continent"] = "EU"
df["continent"] = df["continent"].fillna("Other")

df = df.sort_values(
        by=["Gold", "Silver", "Bronze"],
        ascending=[False, False, False]
    )

df = df.melt(
        id_vars=["country", "continent"],
        value_vars=medal_columns,
        var_name='medal',
        value_name='count'
    )

df = (df.groupby(["continent", "medal"], as_index=False)
      .agg(count=("count", "sum"))
      .reset_index())

fig = px.bar(df, x='continent', y='count', color="medal")
st.plotly_chart(fig)

df = medals_filtered.copy()
df["continent"] = df["country_code"].apply(get_continent_code)
df.loc[df["country_code"] == "KOS", "continent"] = "EU"
df["continent"] = df["continent"].fillna("Other")

fig = px.sunburst(df, path=['continent', 'country_code', 'discipline'], color="continent", title = "Distribution Of Medals By Continent, Country and Discipline")
st.plotly_chart(fig)

medal_ranking_df = medals_total_filtered.sort_values(
        by=["Gold", "Silver", "Bronze"],
        ascending=[False, False, False]
    ).loc[:, ["country_code", "country", "Gold", "Silver", "Bronze"]].head(20).melt(
        id_vars=["country_code", "country"],
        value_vars=medal_columns,
        var_name='medal',
        value_name='count'
    )
medal_ranking_fig = px.bar(medal_ranking_df, x="country", y="count", color="medal", barmode="group", title="Country Ranking By Medals")
st.plotly_chart(medal_ranking_fig)