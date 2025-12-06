import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pycountry_convert as pc
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Global Analysis - Paris 2024",
    page_icon="🗺️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #0066CC;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    [data-testid="stMetricValue"] {
        color: #1f1f1f !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #4a4a4a !important;
        font-weight: 500 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">🗺️ Global Analysis</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Explore Olympic performance across the world</p>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    medals_total = pd.read_csv("data/medals_total.csv")
    medals = pd.read_csv("data/medals.csv")
    nocs = pd.read_csv("data/nocs.csv")
    events = pd.read_csv("data/events.csv")
    return medals_total, medals, nocs, events

medals_total, medals, nocs, events = load_data()

# Function to get continent
def get_continent_code(country_code):
    try:
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        return continent_code
    except:
        return "Other"

def get_continent_name(continent_code):
    continent_mapping = {
        'AF': 'Africa',
        'AS': 'Asia',
        'EU': 'Europe',
        'NA': 'North America',
        'SA': 'South America',
        'OC': 'Oceania',
        'Other': 'Other'
    }
    return continent_mapping.get(continent_code, 'Other')

# Add continent to data
medals_total['continent_code'] = medals_total['country_code'].apply(get_continent_code)
medals_total.loc[medals_total['country_code'] == 'XKX', 'continent_code'] = 'EU'
medals_total['continent'] = medals_total['continent_code'].apply(get_continent_name)

medals['continent_code'] = medals['country_code'].apply(get_continent_code)
medals.loc[medals['country_code'] == 'KOS', 'continent_code'] = 'EU'
medals['continent'] = medals['continent_code'].apply(get_continent_name)

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

# Continent filter (Creative Challenge!)
continents = sorted(medals_total['continent'].dropna().unique())
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
st.sidebar.info("💡 **Tip**: Filter by continent to compare regional performance!")

# Apply filters
filtered_medals_total = medals_total.copy()
filtered_medals = medals.copy()

# Filter by countries
if selected_countries:
    country_codes = nocs[nocs['country'].isin(selected_countries)]['code'].values
    filtered_medals_total = filtered_medals_total[filtered_medals_total['country_code'].isin(country_codes)]
    filtered_medals = filtered_medals[filtered_medals['country_code'].isin(country_codes)]

# Filter by continents
if selected_continents:
    filtered_medals_total = filtered_medals_total[filtered_medals_total['continent'].isin(selected_continents)]
    filtered_medals = filtered_medals[filtered_medals['continent'].isin(selected_continents)]

# Filter by sports/disciplines
if selected_sports:
    filtered_medals = filtered_medals[filtered_medals['discipline'].isin(selected_sports)]

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

# For detailed medals, filter by medal type
medal_type_map = {'Gold': 'Gold Medal', 'Silver': 'Silver Medal', 'Bronze': 'Bronze Medal'}
selected_medal_types = [medal_type_map[m] for m in medal_columns]
filtered_medals = filtered_medals[filtered_medals['medal_type'].isin(selected_medal_types)]

# Recalculate totals based on selected medal types
filtered_medals_total['Total_filtered'] = filtered_medals_total[medal_columns].sum(axis=1)

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_countries = filtered_medals_total['country_code'].nunique()
    st.metric("🌍 Countries", total_countries)

with col2:
    total_medals = filtered_medals_total['Total_filtered'].sum()
    st.metric("🏆 Total Medals", int(total_medals))

with col3:
    total_continents = filtered_medals_total['continent'].nunique()
    st.metric("🌏 Continents", total_continents)

with col4:
    if not filtered_medals_total.empty:
        avg_medals = filtered_medals_total['Total_filtered'].mean()
        st.metric("📊 Avg per Country", f"{avg_medals:.1f}")

st.markdown("---")

# World Medal Map
st.markdown("### 🗺️ World Medal Distribution Map")

if not filtered_medals_total.empty:
    map_df = filtered_medals_total[['country_code', 'country', 'Total_filtered']].copy()
    
    fig_map = px.choropleth(
        map_df,
        locations="country_code",
        color="Total_filtered",
        hover_name="country",
        color_continuous_scale="Viridis",
        title="Total Medals per Country",
        labels={'Total_filtered': 'Medal Count'}
    )
    
    fig_map.update_layout(
        height=500,
        geo=dict(showframe=False, showcoastlines=True, projection_type='natural earth')
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
else:
    st.info("No data available with current filters")

st.markdown("---")

# Medal Hierarchy by Continent
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ☀️ Medal Hierarchy - Sunburst")
    
    if not filtered_medals.empty:
        fig_sunburst = px.sunburst(
            filtered_medals,
            path=['continent', 'country_code', 'discipline'],
            title="Medals: Continent → Country → Discipline",
            height=600
        )
        
        st.plotly_chart(fig_sunburst, use_container_width=True)
    else:
        st.info("No data available with current filters")

with col2:
    st.markdown("### 🔲 Medal Hierarchy - Treemap")
    
    if not filtered_medals.empty:
        fig_treemap = px.treemap(
            filtered_medals,
            path=['continent', 'country_code', 'discipline'],
            title="Medals: Continent → Country → Discipline",
            height=600
        )
        
        st.plotly_chart(fig_treemap, use_container_width=True)
    else:
        st.info("No data available with current filters")

st.markdown("---")

# Continental Analysis
st.markdown("### 🌍 Continental Medal Analysis")

if not filtered_medals_total.empty:
    # Prepare data for continent comparison
    continent_df = filtered_medals_total.groupby('continent')[medal_columns].sum().reset_index()
    
    continent_melted = continent_df.melt(
        id_vars=['continent'],
        value_vars=medal_columns,
        var_name='medal',
        value_name='count'
    )
    
    # Color mapping
    color_map = {
        'Gold': '#FFD700',
        'Silver': '#C0C0C0',
        'Bronze': '#CD7F32'
    }
    
    fig_continent = px.bar(
        continent_melted,
        x='continent',
        y='count',
        color='medal',
        barmode='group',
        title="Medal Distribution by Continent",
        color_discrete_map=color_map,
        labels={'continent': 'Continent', 'count': 'Number of Medals', 'medal': 'Medal Type'}
    )
    
    fig_continent.update_layout(height=500)
    
    st.plotly_chart(fig_continent, use_container_width=True)
else:
    st.info("No data available with current filters")

st.markdown("---")

# Country Ranking
st.markdown("### 🏆 Top 20 Countries - Medal Breakdown")

if not filtered_medals_total.empty:
    # Sort and get top 20
    top_countries = filtered_medals_total.nlargest(20, 'Total_filtered')
    
    top_countries_melted = top_countries.melt(
        id_vars=['country_code', 'country'],
        value_vars=medal_columns,
        var_name='medal',
        value_name='count'
    )
    
    # Color mapping
    color_map = {
        'Gold': '#FFD700',
        'Silver': '#C0C0C0',
        'Bronze': '#CD7F32'
    }
    
    fig_country_ranking = px.bar(
        top_countries_melted,
        x='country',
        y='count',
        color='medal',
        barmode='group',
        title="Top 20 Countries by Medal Count",
        color_discrete_map=color_map,
        labels={'country': 'Country', 'count': 'Number of Medals', 'medal': 'Medal Type'}
    )
    
    fig_country_ranking.update_layout(
        height=600,
        xaxis_tickangle=-45
    )
    
    st.plotly_chart(fig_country_ranking, use_container_width=True)
    
    # Show data table
    with st.expander("📊 View Detailed Rankings"):
        display_df = top_countries[['country', 'continent'] + medal_columns + ['Total_filtered']].copy()
        display_df.columns = ['Country', 'Continent'] + medal_columns + ['Total']
        st.dataframe(display_df.reset_index(drop=True), use_container_width=True)
else:
    st.info("No data available with current filters")

# Performance comparison
st.markdown("---")
st.markdown("### 📊 Regional Performance Insights")

if not filtered_medals_total.empty and len(filtered_medals_total) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        # Top continent
        continent_totals = filtered_medals_total.groupby('continent')['Total_filtered'].sum().sort_values(ascending=False)
        if len(continent_totals) > 0:
            top_continent = continent_totals.index[0]
            top_continent_medals = int(continent_totals.iloc[0])
            st.success(f"🥇 **Leading Continent**: {top_continent} with {top_continent_medals} medals")
    
    with col2:
        # Top country
        if len(filtered_medals_total) > 0:
            top_country = filtered_medals_total.nlargest(1, 'Total_filtered').iloc[0]
            st.success(f"🌟 **Top Country**: {top_country['country']} with {int(top_country['Total_filtered'])} medals")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🗺️ <strong>Paris 2024 Olympics - Global Analysis</strong></p>
    <p>Built with ❤️ using Streamlit | Mapping Olympic Excellence</p>
</div>
""", unsafe_allow_html=True)