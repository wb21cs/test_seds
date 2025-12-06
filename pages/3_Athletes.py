import math
import requests
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import ast
from utils.get_athlete_image import get_athlete_image
import pycountry
import pycountry_convert as pc

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
        
    df = pd.read_csv(path)
    df["disciplines"] = df["disciplines"].apply(safe_parse)
    df["events"] = df["events"].apply(safe_parse)
    df["continent"] = df["country_code"].apply(get_continent_code)


    return df

df = load_df("data/athletes.csv")
athletes = df.copy()

st.title("Athletes")

st.subheader("An Athlete Profile")

selected_athlete = st.selectbox(label="Select an athlete:",
             options=athletes["code"],
             index=None,
             placeholder="Choose an athlete...",
             format_func=lambda opt: str(np.array(athletes.loc[athletes["code"] == opt, "name"])[0])
             )

if selected_athlete:
    athlete = (athletes.loc[
            athletes["code"] == selected_athlete,
            ["name", "country", "height", "weight", "disciplines", "events", "coach"]
        ]
        .iloc[0]
        .to_dict()
    )

    athlete['image'] = get_athlete_image(athlete['name'])
    if isinstance(athlete["coach"], float) and math.isnan(athlete["coach"]):
        athlete["coach"] = "Not available"

    # athlete

    st.subheader("Selected Athlete Profile")

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
        st.markdown(f"**Sport(s):** {", ".join(athlete['disciplines'])}")
        st.markdown(f"**Events(s):** {", ".join(athlete['events'])}")    
        st.markdown(f"**Coach(s):** {athlete['coach'].replace(".<br>", ", ")}")





# age distribution
athletes["age"] = 2024 - pd.to_datetime(athletes["birth_date"]).dt.year

athletes_exploded = athletes.explode("disciplines")
# athletes_exploded

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

st.subheader("Global Athletes Age Distribution")
st.plotly_chart(fig_age)


st.subheader("Gender Distribution")

view_level = st.selectbox(
    "View Gender Distribution By:",
    ["World", "Continent", "Country"]
)

if view_level == "World":
    filtered = athletes

elif view_level == "Continent":
    selected_continent = st.selectbox(
        "Select Continent",
        sorted(athletes["continent"].dropna().unique())
    )
    filtered = athletes[athletes["continent"] == selected_continent]

else:
    selected_country = st.selectbox(
        "Select Country",
        sorted(athletes["country"].dropna().unique())
    )
    filtered = athletes[athletes["country"] == selected_country]

gender_dist = (
    filtered["gender"]
    .value_counts()
    .reset_index()
)

gender_dist.columns = ["gender", "count"]

fig_gender = px.bar(
    gender_dist,
    x="gender",
    y="count",
    title="Gender Distribution of Athletes"
)

st.plotly_chart(fig_gender, width="stretch")



@st.cache_data
def load_medalists():
    medals = pd.read_csv("data/medals.csv")

    countries = set(medals["country"].dropna().unique())

    medals_clean = medals[~medals["name"].isin(countries)]

    top_athletes = (
        medals_clean["name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_athletes.columns = ["athlete", "medal_count"]
    return top_athletes

top_athletes = load_medalists()

fig_top_athletes = px.bar(
    top_athletes,
    x="medal_count",
    y="athlete",
    orientation="h",
    title="Top 10 Athletes by Total Medals"
)

fig_top_athletes.update_layout(yaxis=dict(autorange="reversed"))

st.subheader("Top 10 Athletes by Medals")
st.plotly_chart(fig_top_athletes, width="stretch")