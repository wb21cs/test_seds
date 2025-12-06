import math
import requests
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import ast
import pycountry
import pycountry_convert as pc
import sys
import os

# Add parent directory to path to access utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import get_athlete_image, use fallback if not available
try:
    from utils.get_athlete_image import get_athlete_image
except ImportError:
    # Fallback function if utils module is not found
    def get_athlete_image(athlete_name):
        """
        Placeholder function to get athlete image.
        Replace this with your actual implementation if you have image URLs.
        """
        return Noneimport math
import requests
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import ast
import pycountry
import pycountry_convert as pc

# Function to get athlete image (if available)
def get_athlete_image(athlete_name):
    """
    Placeholder function to get athlete image.
    Replace this with your actual implementation if you have image URLs.
    """
    # You can implement this to return image URLs from a dataset or API
    # For now, returning None as placeholder
    return None

# Page configuration
st.set_page_config(
    page_title="Athlete Performance - Paris 2024",
    page_icon="👤",
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

@st.cache_data
def load_df(path):
    def safe_parse(x):
        if isinstance(x, list):
            return x
        if pd.isna(x):
            return []
        if isinstance(x, str):
            x = x.strip()
            if x.startswith("[") and x.endswith("]"):
                try:
                    return ast.literal_eval(x)
                except:
                    return []
            else:
                return [x]
        return []
    
    def get_continent_code(ioc_code):
        IOC_FIXES = {
            "ALG": "DZA",  # Algeria
            "MAW": "MWI",  # Malawi
            "MAS": "MYS",  # Malaysia
            "MTN": "MRT",  # Mauritania
            "KOS": "XKX",  # Kosovo
            "UAE": "ARE",  # UAE
            "GAM": "GMB",  # Gambia
            "IRI": "IRN",  # Iran
            "GER": "DEU",  # Germany
            "SKN": "KNA",  # St Kits and Nevis
            "CGO": "COG",  # Congo
            "PUR": "PRI",  # Puerto Rico
            "OMA": "OMN",  # Oman
            "ISV": "VIR",  # Virgin Islands
            "LBA": "LBY",  # Libya
            "CAY": "CYM",  # Cayman
            "BER": "BMU",  # Bermuda
            "VIN": "VCT",  # St Vincent
            "ARU": "ABW",  # Aruba
            "CRO": "HRV",  # Croatia
            "PAR": "PRY",  # Paraguay
            "KUW": "KWT",  # Kuwait
            "VAN": "VUT",  # Vanuatu
            "BHU": "BTN",  # Bhutan
            "BAN": "BGD",  # Bangladesh
            "NED": "NLD",  # Netherlnds
            "GEQ": "GNQ",  # Equatorial Guniea
            "GUI": "GIN",  # Guniea
            "MYA": "MMR",  # Myanmar
            "CAM": "KHM",  # Cambodia
            "LES": "LSO",  # Lesotho
            "FIJ": "FJI",  # Fiji
            "CRC": "CRI",  # Costa Rica
            "BUL": "BGR",  # Bulgaria
            "TPE": "TWN",  # Taiwan
            "MRI": "MUS",  # Mauritius
            "GRN": "GRD",  # Grenada
            "NGR": "NGA",  # Nigeria
            "GBS": "GNB",  # Guinea-Bissau
            "ZIM": "ZWE",  # Zimbabwe
            "IVB": "VGB",  # Virgin Islands, B
            "VIE": "VNM",  # Vietnam
            "ESA": "SLV",  # El Salvador
            "RSA": "ZAF",  # South Africa
            "BUR": "BFA",  # Burkina Faso
            "INA": "IDN",  # Indonesia
            "DEN": "DNK",  # Denmark
            "SUD": "SDN",  # Sudan
            "ANG": "AGO",  # Angola
            "TAN": "TZA",  # Tanzania
            "BAR": "BRB",  # Barbados
            "SEY": "SYC",  # Seychelles
            "MON": "MCO",  # Monaco
            "NIG": "NER",  # Niger
            "CHI": "CHL",  # Chile
            "BAH": "BHS",  # Bahamas
            "URU": "URY",  # Uruguay
            "MGL": "MNG",  # Mongolia
            "PLE": "PSE",  # Palestine
            "ZAM": "ZMB",  # Zambia
            "POR": "PRT",  # Portogal
            "NCA": "NIC",  # Nicaragua
            "BOT": "BWA",  # Botswana
            "GUA": "GTM",  # Guatemala
            "GRE": "GRC",  # Greece
            "KSA": "SAU",  # Saudi Arabia
            "BRU": "BRN",  # Brunei Darussalam
            "HAI": "HTI",  # Haiti
            "MAD": "MDG",  # Madagascar
            "HON": "HND",  # Honduras
            "LAT": "LVA",  # Latvia
            "SUI": "CHE",  # Switzerland
            "SLO": "SVN",  # Slovenia
            "NEP": "NPL",  # Nepal
            "ANT": "ATG",  # Antigua and Barbuda
            "CHA": "TCD",  # Chad
            "BIZ": "BLZ",  # Belize
            "SOL": "SLB",  # Solomon Islands
            "CHA": "TCD",  # Chad
            "TOG": "TGO",  # Togo TOG
            "SRI": "LKA",  # Sri Lanka SRI
            "TGA": "TON",  # Tonga TGA
            "ASA": "ASM",  # American Samoa ASA
            "SAM": "WsM",  # Samoa SAM
            "PHI": "PHL",  # Philippines PHI
        }

        try:
            iso3 = IOC_FIXES.get(ioc_code, ioc_code)

            if iso3 == "TLS":
                return "AS"
            if iso3 in ["AIN", "EOR"]:
                return "Other"

            country = pycountry.countries.get(alpha_3=iso3)
            if not country:
                return None

            continent_code = pc.country_alpha2_to_continent_code(country.alpha_2)
            return continent_code

        except:
            return None
    
    def get_continent_name(continent_code):
        continent_mapping = {
            'AF': 'Africa',
            'AS': 'Asia',
            'EU': 'Europe',
            'NA': 'North America',
            'SA': 'South America',
            'OC': 'Oceania',
            None: 'Other'
        }
        return continent_mapping.get(continent_code, 'Other')
        
    df = pd.read_csv(path)
    df["disciplines"] = df["disciplines"].apply(safe_parse)
    df["events"] = df["events"].apply(safe_parse)
    df["continent_code"] = df["country_code"].apply(get_continent_code)
    df["continent"] = df["continent_code"].apply(get_continent_name)

    return df

# Load data
df = load_df("data/athletes.csv")
athletes = df.copy()

@st.cache_data
def load_additional_data():
    nocs = pd.read_csv("data/nocs.csv")
    events = pd.read_csv("data/events.csv")
    medals = pd.read_csv("data/medals.csv")
    return nocs, events, medals

nocs, events, medals = load_additional_data()

# Title
st.markdown('<p class="main-header">👤 Athlete Performance</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">The human story behind the medals</p>', unsafe_allow_html=True)

# SIDEBAR FILTERS
st.sidebar.header("🎯 Global Filters")

# Country filter
countries = sorted(nocs['country'].dropna().unique())
selected_countries = st.sidebar.multiselect(
    "🌍 Select Countries",
    countries,
    default=[],
    help="Filter athletes by specific countries"
)

# Sport filter
sports = sorted(events['sport'].dropna().unique())
selected_sports = st.sidebar.multiselect(
    "🏅 Select Sports",
    sports,
    default=[],
    help="Filter athletes by specific sports"
)

# Continent filter (Creative Challenge!)
continents = sorted(athletes['continent'].dropna().unique())
selected_continents = st.sidebar.multiselect(
    "🌏 Select Continents (Creative Filter!)",
    continents,
    default=[],
    help="Filter athletes by continent"
)

# Medal type filter
st.sidebar.subheader("🥇 Medal Types")
show_gold = st.sidebar.checkbox("Gold", value=True)
show_silver = st.sidebar.checkbox("Silver", value=True)
show_bronze = st.sidebar.checkbox("Bronze", value=True)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Use filters to explore athletes from specific regions or sports!")

# Apply filters
filtered_athletes = athletes.copy()

# Filter by countries
if selected_countries:
    country_codes = nocs[nocs['country'].isin(selected_countries)]['code'].values
    filtered_athletes = filtered_athletes[filtered_athletes['country_code'].isin(country_codes)]

# Filter by continents
if selected_continents:
    filtered_athletes = filtered_athletes[filtered_athletes['continent'].isin(selected_continents)]

# Filter by sports/disciplines
if selected_sports:
    # Filter athletes who have any of the selected sports in their disciplines list
    filtered_athletes = filtered_athletes[
        filtered_athletes['disciplines'].apply(
            lambda x: any(sport in x for sport in selected_sports) if isinstance(x, list) else False
        )
    ]

# Filter medals by medal types
medal_type_map = {'Gold': 'Gold Medal', 'Silver': 'Silver Medal', 'Bronze': 'Bronze Medal'}
selected_medal_types = []
if show_gold:
    selected_medal_types.append('Gold Medal')
if show_silver:
    selected_medal_types.append('Silver Medal')
if show_bronze:
    selected_medal_types.append('Bronze Medal')

if not selected_medal_types:
    selected_medal_types = ['Gold Medal', 'Silver Medal', 'Bronze Medal']

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Total Athletes", f"{len(filtered_athletes):,}")

with col2:
    unique_countries = filtered_athletes['country'].nunique()
    st.metric("🌍 Countries", unique_countries)

with col3:
    # Count unique disciplines
    all_disciplines = []
    for disc_list in filtered_athletes['disciplines']:
        if isinstance(disc_list, list):
            all_disciplines.extend(disc_list)
    unique_disciplines = len(set(all_disciplines))
    st.metric("🏅 Disciplines", unique_disciplines)

with col4:
    if 'gender' in filtered_athletes.columns:
        female_count = len(filtered_athletes[filtered_athletes['gender'] == 'Female'])
        male_count = len(filtered_athletes[filtered_athletes['gender'] == 'Male'])
        if female_count + male_count > 0:
            female_ratio = (female_count / (female_count + male_count)) * 100
            st.metric("🚺 Female Ratio", f"{female_ratio:.1f}%")

st.markdown("---")

st.subheader("🎯 Athlete Profile Search")

selected_athlete = st.selectbox(label="Select an athlete:",
             options=filtered_athletes["code"],
             index=None,
             placeholder="Choose an athlete...",
             format_func=lambda opt: str(np.array(filtered_athletes.loc[filtered_athletes["code"] == opt, "name"])[0])
             )

if selected_athlete:
    athlete = (filtered_athletes.loc[
            filtered_athletes["code"] == selected_athlete,
            ["name", "country", "height", "weight", "disciplines", "events", "coach"]
        ]
        .iloc[0]
        .to_dict()
    )

    athlete['image'] = get_athlete_image(athlete['name'])
    if isinstance(athlete["coach"], float) and math.isnan(athlete["coach"]):
        athlete["coach"] = "Not available"

    st.subheader("✨ Selected Athlete Profile")

    col1, col2 = st.columns([1, 3], gap="large")

    with col1:
        if athlete["image"]:
            @st.cache_data
            def fetch_image(url):
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.content
            
            st.image(fetch_image(athlete["image"]), width=160)
        else:
            st.markdown(
                """
                <div style="
                    width:160px;
                    height:160px;
                    border-radius:50%;
                    background:#e5e7eb;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:48px;
                    color:#6b7280;">
                    👤
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        st.markdown(f"### {athlete['name']}")
        st.markdown(f"**Country:** {athlete['country']}")
        st.markdown(f"**Height:** {athlete['height']} cm")
        st.markdown(f"**Weight:** {athlete['weight']} kg")
        disciplines_str = ', '.join(athlete['disciplines'])
        st.markdown(f"**Sport(s):** {disciplines_str}")
        events_str = ', '.join(athlete['events'])
        st.markdown(f"**Events(s):** {events_str}")
        coach_str = athlete['coach'].replace('.<br>', ', ')
        st.markdown(f"**Coach(s):** {coach_str}")

st.markdown("---")

# age distribution
filtered_athletes["age"] = 2024 - pd.to_datetime(filtered_athletes["birth_date"]).dt.year

athletes_exploded = filtered_athletes.explode("disciplines")

fig_age = px.violin(
    athletes_exploded,
    x="disciplines",
    y="age",
    color="gender",
    box=True,
    points="all",
    title="Athlete Age Distribution by Sport and Gender"
)

fig_age.update_layout(xaxis_title="Sport", yaxis_title="Age")

st.subheader("📊 Global Athletes Age Distribution")
st.plotly_chart(fig_age, use_container_width=True)

st.markdown("---")

st.subheader("👥 Gender Distribution")

view_level = st.selectbox(
    "View Gender Distribution By:",
    ["World", "Continent", "Country"]
)

if view_level == "World":
    filtered_for_gender = filtered_athletes

elif view_level == "Continent":
    available_continents = sorted(filtered_athletes["continent"].dropna().unique())
    if available_continents:
        selected_continent = st.selectbox(
            "Select Continent",
            available_continents
        )
        filtered_for_gender = filtered_athletes[filtered_athletes["continent"] == selected_continent]
    else:
        st.warning("No continents available with current filters")
        filtered_for_gender = pd.DataFrame()

else:
    available_countries = sorted(filtered_athletes["country"].dropna().unique())
    if available_countries:
        selected_country = st.selectbox(
            "Select Country",
            available_countries
        )
        filtered_for_gender = filtered_athletes[filtered_athletes["country"] == selected_country]
    else:
        st.warning("No countries available with current filters")
        filtered_for_gender = pd.DataFrame()

if not filtered_for_gender.empty:
    gender_dist = (
        filtered_for_gender["gender"]
        .value_counts()
        .reset_index()
    )

    gender_dist.columns = ["gender", "count"]

    fig_gender = px.bar(
        gender_dist,
        x="gender",
        y="count",
        title=f"Gender Distribution of Athletes - {view_level}",
        color="gender",
        color_discrete_map={"Male": "#3b82f6", "Female": "#ec4899"}
    )

    st.plotly_chart(fig_gender, use_container_width=True)
else:
    st.info("No data available for gender distribution with current filters")

st.markdown("---")

@st.cache_data
def load_medalists():
    medals_df = pd.read_csv("data/medals.csv")

    countries = set(medals_df["country"].dropna().unique())

    medals_clean = medals_df[~medals_df["name"].isin(countries)]

    top_athletes = (
        medals_clean["name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_athletes.columns = ["athlete", "medal_count"]
    return top_athletes, medals_df

top_athletes_data, medals_data = load_medalists()

# Filter top athletes based on filters
filtered_medals = medals_data.copy()

# Apply country filter to medals
if selected_countries:
    country_codes = nocs[nocs['country'].isin(selected_countries)]['code'].values
    filtered_medals = filtered_medals[filtered_medals['country_code'].isin(country_codes)]

# Apply continent filter to medals
if selected_continents:
    # Add continent to medals if not present
    if 'continent_code' not in filtered_medals.columns:
        def get_continent_code_simple(country_code):
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
        
        filtered_medals['continent_code'] = filtered_medals['country_code'].apply(get_continent_code_simple)
        filtered_medals.loc[filtered_medals['country_code'] == 'KOS', 'continent_code'] = 'EU'
        filtered_medals['continent'] = filtered_medals['continent_code'].apply(get_continent_name)
    
    filtered_medals = filtered_medals[filtered_medals['continent'].isin(selected_continents)]

# Apply sport filter to medals
if selected_sports:
    filtered_medals = filtered_medals[filtered_medals['discipline'].isin(selected_sports)]

# Apply medal type filter
filtered_medals = filtered_medals[filtered_medals['medal_type'].isin(selected_medal_types)]

# Calculate top athletes from filtered medals
countries_set = set(filtered_medals["country"].dropna().unique())
medals_clean = filtered_medals[~filtered_medals["name"].isin(countries_set)]

if not medals_clean.empty:
    top_athletes_filtered = (
        medals_clean["name"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_athletes_filtered.columns = ["athlete", "medal_count"]

    fig_top_athletes = px.bar(
        top_athletes_filtered,
        x="medal_count",
        y="athlete",
        orientation="h",
        title="Top 10 Athletes by Total Medals",
        color="medal_count",
        color_continuous_scale="Viridis"
    )

    fig_top_athletes.update_layout(yaxis=dict(autorange="reversed"))

    st.subheader("🏆 Top 10 Athletes by Medals")
    st.plotly_chart(fig_top_athletes, use_container_width=True)
else:
    st.info("No medal data available with current filters")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>👤 <strong>Paris 2024 Olympics - Athlete Performance</strong></p>
    <p>Built with ❤️ using Streamlit | Celebrating Athletic Excellence</p>
</div>
""", unsafe_allow_html=True)