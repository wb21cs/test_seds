import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry_convert as pc
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Overview - Paris 2024",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS for better styling
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

# Load data
@st.cache_data
def load_data():
    athletes = pd.read_csv("data/athletes.csv")
    nocs = pd.read_csv("data/nocs.csv")
    events = pd.read_csv("data/events.csv")
    medals_total = pd.read_csv("data/medals_total.csv")
    medals = pd.read_csv("data/medals.csv")
    return athletes, nocs, events, medals_total, medals

athletes, nocs, events, medals_total, medals = load_data()

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
if 'continent' not in medals_total.columns:
    medals_total['continent_code'] = medals_total['country_code'].apply(get_continent_code)
    medals_total.loc[medals_total['country_code'] == 'XKX', 'continent_code'] = 'EU'
    medals_total['continent'] = medals_total['continent_code'].apply(get_continent_name)

if 'continent' not in medals.columns:
    medals['continent_code'] = medals['country_code'].apply(get_continent_code)
    medals.loc[medals['country_code'] == 'KOS', 'continent_code'] = 'EU'
    medals['continent'] = medals['continent_code'].apply(get_continent_name)

# Title
st.markdown('<p class="main-header">🏠 Paris 2024 Olympics - Command Center</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your comprehensive dashboard for Olympic excellence</p>', unsafe_allow_html=True)

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
    help="Filter data by continent - a powerful way to analyze regional performance!"
)

# Medal type filter
st.sidebar.subheader("🥇 Medal Types")
show_gold = st.sidebar.checkbox("Gold", value=True)
show_silver = st.sidebar.checkbox("Silver", value=True)
show_bronze = st.sidebar.checkbox("Bronze", value=True)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Use filters to explore specific countries, sports, or regions!")

# Apply filters
filtered_medals_total = medals_total.copy()
filtered_medals = medals.copy()
filtered_events = events.copy()
filtered_athletes = athletes.copy()

# Filter by countries
if selected_countries:
    country_codes = nocs[nocs['country'].isin(selected_countries)]['code'].values
    filtered_medals_total = filtered_medals_total[filtered_medals_total['country_code'].isin(country_codes)]
    filtered_medals = filtered_medals[filtered_medals['country_code'].isin(country_codes)]
    filtered_athletes = filtered_athletes[filtered_athletes['country_code'].isin(country_codes)]

# Filter by continents
if selected_continents:
    filtered_medals_total = filtered_medals_total[filtered_medals_total['continent'].isin(selected_continents)]
    filtered_medals = filtered_medals[filtered_medals['continent'].isin(selected_continents)]

# Filter by sports
if selected_sports:
    filtered_events = filtered_events[filtered_events['sport'].isin(selected_sports)]
    filtered_medals = filtered_medals[filtered_medals['discipline'].isin(selected_sports)]
    # Filter athletes by disciplines
    filtered_athletes = filtered_athletes[
        filtered_athletes['disciplines'].str.contains('|'.join(selected_sports), case=False, na=False)
    ]

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

# Filter medals dataframe by medal type
medal_type_map = {'Gold': 'Gold Medal', 'Silver': 'Silver Medal', 'Bronze': 'Bronze Medal'}
selected_medal_types = [medal_type_map[m] for m in medal_columns]
filtered_medals = filtered_medals[filtered_medals['medal_type'].isin(selected_medal_types)]

# Calculate KPIs
nb_athletes = len(filtered_athletes)
nb_countries = filtered_medals_total['country_code'].nunique() if not filtered_medals_total.empty else 0
nb_sports = filtered_events['sport_code'].nunique() if not filtered_events.empty else 0
total_medals = filtered_medals_total[medal_columns].sum().sum() if not filtered_medals_total.empty else 0
nb_events = len(filtered_events)

# KPI Metrics Section
st.markdown("### 📊 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("👥 Athletes", f"{nb_athletes:,}")

with col2:
    st.metric("🌍 Countries", f"{nb_countries:,}")

with col3:
    st.metric("🏅 Sports", f"{nb_sports:,}")

with col4:
    st.metric("🏆 Medals Awarded", f"{int(total_medals):,}")

with col5:
    st.metric("🎯 Events", f"{nb_events:,}")

st.markdown("---")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🥇 Global Medal Distribution")
    
    if not filtered_medals_total.empty:
        medal_counts = filtered_medals_total[medal_columns].sum().reset_index()
        medal_counts.columns = ['Medal', 'Count']
        
        # Color mapping for medals
        color_map = {
            'Gold': '#FFD700',
            'Silver': '#C0C0C0',
            'Bronze': '#CD7F32'
        }
        
        medal_count_fig = px.bar(
            medal_counts,
            x="Medal",
            y="Count",
            color="Medal",
            title="Distribution of Medal Types",
            color_discrete_map=color_map,
            text="Count"
        )
        
        medal_count_fig.update_traces(textposition='outside')
        medal_count_fig.update_layout(
            showlegend=False,
            height=400,
            xaxis_title="Medal Type",
            yaxis_title="Number of Medals"
        )
        
        st.plotly_chart(medal_count_fig, use_container_width=True)
    else:
        st.info("No data available with current filters")

with col2:
    st.markdown("### 🏆 Top 10 Countries - Medal Standings")
    
    if not filtered_medals_total.empty:
        # Calculate total for sorting
        filtered_medals_total['Total_filtered'] = filtered_medals_total[medal_columns].sum(axis=1)
        
        medal_ranking_df = filtered_medals_total.nlargest(10, 'Total_filtered')
        medal_ranking_df = medal_ranking_df.melt(
            id_vars=["country_code", "country"],
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
        
        medal_ranking_fig = px.bar(
            medal_ranking_df,
            x="country",
            y="count",
            color="medal",
            barmode="group",
            title="Top 10 Countries by Medal Count",
            color_discrete_map=color_map,
            labels={'country': 'Country', 'count': 'Number of Medals', 'medal': 'Medal Type'}
        )
        
        medal_ranking_fig.update_layout(
            height=400,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(medal_ranking_fig, use_container_width=True)
    else:
        st.info("No data available with current filters")

# Additional insights section
st.markdown("---")
st.markdown("### 🌍 Continental Performance Overview")

if not filtered_medals_total.empty and 'continent' in filtered_medals_total.columns:
    continent_medals = filtered_medals_total.groupby('continent')[medal_columns].sum().reset_index()
    continent_medals['Total'] = continent_medals[medal_columns].sum(axis=1)
    continent_medals = continent_medals.sort_values('Total', ascending=True)
    
    fig_continent = px.bar(
        continent_medals,
        y='continent',
        x='Total',
        orientation='h',
        title="Total Medals by Continent",
        color='Total',
        color_continuous_scale='Viridis',
        text='Total'
    )
    
    fig_continent.update_traces(textposition='outside')
    fig_continent.update_layout(
        height=400,
        showlegend=False,
        xaxis_title="Total Medals",
        yaxis_title="Continent"
    )
    
    st.plotly_chart(fig_continent, use_container_width=True)

# Quick Stats
st.markdown("---")
st.markdown("### 📈 Quick Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    if not filtered_medals_total.empty:
        avg_medals_per_country = filtered_medals_total[medal_columns].sum(axis=1).mean()
        st.metric("📊 Avg Medals per Country", f"{avg_medals_per_country:.1f}")

with col2:
    if not filtered_athletes.empty and 'gender' in filtered_athletes.columns:
        gender_counts = filtered_athletes['gender'].value_counts()
        male_count = gender_counts.get('Male', 0)
        female_count = gender_counts.get('Female', 0)
        if male_count + female_count > 0:
            gender_ratio = (female_count / (male_count + female_count)) * 100
            st.metric("🚺 Female Athlete Ratio", f"{gender_ratio:.1f}%")

with col3:
    if not filtered_events.empty:
        events_per_sport = len(filtered_events) / nb_sports if nb_sports > 0 else 0
        st.metric("🎯 Avg Events per Sport", f"{events_per_sport:.1f}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🏠 <strong>Paris 2024 Olympics Dashboard</strong></p>
    <p>Built with ❤️ using Streamlit | Celebrating Olympic Excellence</p>
</div>
""", unsafe_allow_html=True)