import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Olympic Torch Route",
    page_icon="🔥",
    layout="wide"
)

# Title and description
st.title("🔥 Olympic Torch Relay Journey")
st.markdown("""
Trace the inspiring path of the Olympic flame as it traveled across France, 
carrying the spirit of the Games to communities nationwide before reaching Paris 2024.
""")

# Pre-defined coordinates for major French cities
CITY_COORDINATES = {
    'Paris': (48.8566, 2.3522),
    'Marseille': (43.2965, 5.3698),
    'Lyon': (45.7640, 4.8357),
    'Toulouse': (43.6047, 1.4442),
    'Nice': (43.7102, 7.2620),
    'Nantes': (47.2184, -1.5536),
    'Strasbourg': (48.5734, 7.7521),
    'Montpellier': (43.6108, 3.8767),
    'Bordeaux': (44.8378, -0.5792),
    'Lille': (50.6292, 3.0573),
    'Rennes': (48.1173, -1.6778),
    'Reims': (49.2583, 4.0317),
    'Le Havre': (49.4944, 0.1079),
    'Saint-Étienne': (45.4397, 4.3872),
    'Toulon': (43.1242, 5.9280),
    'Grenoble': (45.1885, 5.7245),
    'Dijon': (47.3220, 5.0415),
    'Angers': (47.4784, -0.5632),
    'Nîmes': (43.8367, 4.3601),
    'Villeurbanne': (45.7661, 4.8792),
    'Clermont-Ferrand': (45.7772, 3.0870),
    'Le Mans': (48.0077, 0.1984),
    'Aix-en-Provence': (43.5297, 5.4474),
    'Brest': (48.3904, -4.4861),
    'Tours': (47.3941, 0.6848),
    'Amiens': (49.8941, 2.2958),
    'Limoges': (45.8336, 1.2611),
    'Annecy': (45.8992, 6.1294),
    'Perpignan': (42.6886, 2.8948),
    'Besançon': (47.2380, 6.0243),
    'Orléans': (47.9029, 1.9093),
    'Metz': (49.1193, 6.1757),
    'Rouen': (49.4432, 1.0993),
    'Mulhouse': (47.7508, 7.3359),
    'Caen': (49.1829, -0.3707),
    'Nancy': (48.6921, 6.1844),
    'Saint-Denis': (48.9356, 2.3539),
    'Argenteuil': (48.9475, 2.2514),
    'Montreuil': (48.8634, 2.4432),
    'Roubaix': (50.6942, 3.1746),
    'Dunkerque': (51.0343, 2.3768),
    'Avignon': (43.9493, 4.8055),
    'Poitiers': (46.5802, 0.3404),
    'Versailles': (48.8048, 2.1203),
    'Courbevoie': (48.8969, 2.2539),
    'Colombes': (48.9226, 2.2531),
    'Aulnay-sous-Bois': (48.9534, 2.4894),
    'La Rochelle': (46.1603, -1.1511),
    'Calais': (50.9513, 1.8587),
    'Cannes': (43.5528, 7.0174),
    'Antibes': (43.5808, 7.1239),
    'Saint-Maur-des-Fossés': (48.7997, 2.4947),
    'Béziers': (43.3440, 3.2150),
    'Bourges': (47.0844, 2.3964),
    'Saint-Nazaire': (47.2733, -2.2134),
    'Valence': (44.9334, 4.8924),
    'Lorient': (47.7482, -3.3706),
    'Quimper': (47.9960, -4.0970),
    'Troyes': (48.2973, 4.0744),
    'Chambéry': (45.5646, 5.9178),
    'Niort': (46.3236, -0.4594),
    'Villefranche-sur-Saône': (45.9858, 4.7180),
    'Saint-Quentin': (49.8484, 3.2872),
    'Beauvais': (49.4295, 2.0807),
    'Cholet': (47.0608, -0.8790),
    'Vannes': (47.6586, -2.7603),
    'Pau': (43.2951, -0.3708),
    'Bayonne': (43.4933, -1.4748),
    'Ajaccio': (41.9267, 8.7369),
    'Bastia': (42.7026, 9.4502),
    'La Seyne-sur-Mer': (43.1010, 5.8815),
    'Hyères': (43.1203, 6.1288),
    'Carcassonne': (43.2130, 2.3491),
    'Blois': (47.5867, 1.3352),
    'Arles': (43.6768, 4.6306),
    'Chartres': (48.4469, 1.4850),
    'Mâcon': (46.3067, 4.8328),
    'Épinal': (48.1745, 6.4499),
    'Châlons-en-Champagne': (48.9566, 4.3653),
}

# Load the torch route data
@st.cache_data
def load_torch_data():
    try:
        df = pd.read_csv('data/torch_route.csv')
        return df
    except FileNotFoundError:
        st.error("⚠️ torch_route.csv file not found. Please ensure the file is in the correct directory.")
        return None

# Add coordinates to dataframe
@st.cache_data
def add_coordinates(df):
    """Add lat/lon coordinates based on city names"""
    coords = []
    for city in df['city']:
        # Handle NaN or non-string values
        if pd.isna(city) or not isinstance(city, str):
            # Default to Paris if city is missing
            coords.append({'lat': 48.8566, 'lon': 2.3522})
            continue
            
        # Try exact match first
        if city in CITY_COORDINATES:
            lat, lon = CITY_COORDINATES[city]
            coords.append({'lat': lat, 'lon': lon})
        else:
            # Try case-insensitive match
            city_lower = city.lower()
            matched = False
            for known_city, (lat, lon) in CITY_COORDINATES.items():
                if known_city.lower() == city_lower:
                    coords.append({'lat': lat, 'lon': lon})
                    matched = True
                    break
            
            if not matched:
                # Default to Paris if city not found
                coords.append({'lat': 48.8566, 'lon': 2.3522})
    
    coords_df = pd.DataFrame(coords)
    return pd.concat([df, coords_df], axis=1)

df_torch = load_torch_data()

if df_torch is not None:
    # Add coordinates
    df_torch = add_coordinates(df_torch)
    
    # Display dataset info
    with st.expander("📊 Dataset Information"):
        st.write(f"**Total Locations:** {len(df_torch)}")
        st.write(f"**Date Range:** {df_torch['date_start'].min()} to {df_torch['date_end'].max()}")
        st.dataframe(df_torch[['stage_number', 'city', 'title', 'date_start', 'date_end', 'tag']].head(10))
    
    # Sidebar filters
    st.sidebar.header("🎛️ Map Controls")
    
    # Map style selection
    map_style = st.sidebar.selectbox(
        "Map Style",
        ["open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain"],
        index=0
    )
    
    # Visualization type
    viz_type = st.sidebar.radio(
        "Visualization Type",
        ["🔥 Animated Journey", "🗺️ Full Route", "🎯 Stage Numbers"],
        index=1
    )
    
    # Date filter
    df_torch['date_start'] = pd.to_datetime(df_torch['date_start'], errors='coerce')
    if df_torch['date_start'].notna().any():
        min_date = df_torch['date_start'].min().date()
        max_date = df_torch['date_start'].max().date()
        
        date_range = st.sidebar.date_input(
            "📅 Filter by Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        if len(date_range) == 2:
            df_filtered = df_torch[
                (df_torch['date_start'].dt.date >= date_range[0]) &
                (df_torch['date_start'].dt.date <= date_range[1])
            ].copy()
        else:
            df_filtered = df_torch.copy()
    else:
        df_filtered = df_torch.copy()
    
    # Tag filter
    if 'tag' in df_torch.columns:
        unique_tags = df_torch['tag'].dropna().unique().tolist()
        if len(unique_tags) > 0:
            selected_tags = st.sidebar.multiselect(
                "🏷️ Filter by Tag",
                options=unique_tags,
                default=unique_tags
            )
            if selected_tags:
                df_filtered = df_filtered[df_filtered['tag'].isin(selected_tags)]
    
    # Sort by stage number
    df_filtered = df_filtered.sort_values('stage_number').reset_index(drop=True)
    
    # Create columns for layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🗺️ Interactive Map")
        
        if len(df_filtered) > 0:
            # Create hover text
            df_filtered['hover_text'] = df_filtered.apply(
                lambda row: (
                    f"<b>🏙️ {row['city']}</b><br>" +
                    f"<b>Stage:</b> {int(row['stage_number']) if pd.notna(row['stage_number']) else 'N/A'}<br>" +
                    f"<b>📅 Date:</b> {row['date_start'].strftime('%b %d, %Y') if pd.notna(row['date_start']) else 'N/A'}<br>" +
                    f"<b>🎪 Event:</b> {row['title'][:60]}{'...' if len(str(row['title'])) > 60 else ''}"
                ),
                axis=1
            )
            
            # Calculate center
            center_lat = df_filtered['lat'].mean()
            center_lon = df_filtered['lon'].mean()
            
            # Different visualizations
            if "Animated" in viz_type:
                # Animated scatter map
                fig = px.scatter_mapbox(
                    df_filtered,
                    lat='lat',
                    lon='lon',
                    hover_name='city',
                    animation_frame='stage_number',
                    color='stage_number',
                    size=[20]*len(df_filtered),
                    zoom=5.5,
                    height=650,
                    color_continuous_scale='Hot',
                    title="🔥 Torch Relay Animation - Click Play!"
                )
                
                # Add route line
                fig.add_trace(
                    go.Scattermapbox(
                        lat=df_filtered['lat'],
                        lon=df_filtered['lon'],
                        mode='lines',
                        line=dict(width=2, color='rgba(255, 107, 53, 0.6)'),
                        name='Complete Route',
                        hoverinfo='skip',
                        showlegend=False
                    )
                )
                
            elif "Full Route" in viz_type:
                # Full route with markers
                fig = go.Figure()
                
                # Route line
                fig.add_trace(
                    go.Scattermapbox(
                        lat=df_filtered['lat'],
                        lon=df_filtered['lon'],
                        mode='lines',
                        line=dict(width=4, color='#FF6B35'),
                        name='Torch Route',
                        hoverinfo='skip'
                    )
                )
                
                # All stops
                fig.add_trace(
                    go.Scattermapbox(
                        lat=df_filtered['lat'],
                        lon=df_filtered['lon'],
                        mode='markers',
                        marker=dict(
                            size=10,
                            color='#FFD700',
                            opacity=0.8
                        ),
                        text=df_filtered['hover_text'],
                        hoverinfo='text',
                        name='Stops',
                        showlegend=False
                    )
                )
                
                # Start marker
                fig.add_trace(
                    go.Scattermapbox(
                        lat=[df_filtered.iloc[0]['lat']],
                        lon=[df_filtered.iloc[0]['lon']],
                        mode='markers',
                        marker=dict(size=25, color='#00FF00', symbol='star'),
                        name='Start',
                        text=[f"🏁 START<br>{df_filtered.iloc[0]['city']}"],
                        hoverinfo='text'
                    )
                )
                
                # Finish marker
                fig.add_trace(
                    go.Scattermapbox(
                        lat=[df_filtered.iloc[-1]['lat']],
                        lon=[df_filtered.iloc[-1]['lon']],
                        mode='markers',
                        marker=dict(size=25, color='#FF0000', symbol='star'),
                        name='Finish',
                        text=[f"🎯 FINISH<br>{df_filtered.iloc[-1]['city']}"],
                        hoverinfo='text'
                    )
                )
                
                fig.update_layout(
                    mapbox=dict(
                        style=map_style,
                        center=dict(lat=center_lat, lon=center_lon),
                        zoom=5.5
                    ),
                    height=650,
                    margin={"r":0,"t":0,"l":0,"b":0},
                    showlegend=True
                )
                
            else:  # Stage Numbers
                fig = go.Figure()
                
                # Route line
                fig.add_trace(
                    go.Scattermapbox(
                        lat=df_filtered['lat'],
                        lon=df_filtered['lon'],
                        mode='lines',
                        line=dict(width=3, color='#FF6B35'),
                        name='Route',
                        hoverinfo='skip',
                        showlegend=False
                    )
                )
                
                # Numbered markers
                colors = px.colors.sequential.Hot
                for idx, row in df_filtered.iterrows():
                    stage = int(row['stage_number']) if pd.notna(row['stage_number']) else idx + 1
                    color_idx = min(int((idx / len(df_filtered)) * (len(colors)-1)), len(colors)-1)
                    
                    fig.add_trace(
                        go.Scattermapbox(
                            lat=[row['lat']],
                            lon=[row['lon']],
                            mode='markers+text',
                            marker=dict(size=18, color=colors[color_idx]),
                            text=[str(stage)],
                            textposition='middle center',
                            textfont=dict(color='white', size=9, family='Arial Black'),
                            hovertext=row['hover_text'],
                            hoverinfo='text',
                            showlegend=False
                        )
                    )
                
                fig.update_layout(
                    mapbox=dict(
                        style=map_style,
                        center=dict(lat=center_lat, lon=center_lon),
                        zoom=5.5
                    ),
                    height=650,
                    margin={"r":0,"t":0,"l":0,"b":0}
                )
            
            # Update layout
            fig.update_layout(mapbox_style=map_style)
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("⚠️ No data to display with current filters.")
    
    with col2:
        st.subheader("📈 Journey Stats")
        
        if len(df_filtered) > 0:
            # Key metrics
            st.metric("🏙️ Total Stops", len(df_filtered))
            st.metric("🗓️ Unique Cities", df_filtered['city'].nunique())
            
            # Date range
            if df_filtered['date_start'].notna().any():
                start_date = df_filtered['date_start'].min()
                end_date = df_filtered['date_start'].max()
                duration = (end_date - start_date).days
                st.metric("⏱️ Duration", f"{duration} days")
            
            # Calculate distance
            from math import radians, sin, cos, sqrt, atan2
            
            def haversine(lat1, lon1, lat2, lon2):
                R = 6371
                lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * atan2(sqrt(a), sqrt(1-a))
                return R * c
            
            total_distance = sum(
                haversine(
                    df_filtered.iloc[i]['lat'], df_filtered.iloc[i]['lon'],
                    df_filtered.iloc[i+1]['lat'], df_filtered.iloc[i+1]['lon']
                )
                for i in range(len(df_filtered) - 1)
            )
            
            st.metric("🛣️ Distance", f"{total_distance:,.0f} km")
            
            # Tags distribution
            if 'tag' in df_filtered.columns and df_filtered['tag'].notna().any():
                st.markdown("---")
                st.markdown("### 🏷️ Event Tags")
                tag_counts = df_filtered['tag'].value_counts()
                for tag, count in tag_counts.head(5).items():
                    st.write(f"**{tag}**: {count}")
        
        st.markdown("---")
        st.markdown("### 🔥 About")
        st.markdown("""
        The Olympic torch relay brings the Olympic flame from Olympia, Greece 
        to the host city, uniting people along its path.
        """)
    
    # Timeline section
    st.markdown("---")
    st.subheader("📅 Torch Relay Timeline")
    
    if df_filtered['date_start'].notna().any():
        # Prepare timeline data
        timeline_df = df_filtered[['city', 'date_start', 'title', 'stage_number']].copy()
        timeline_df['date_start'] = pd.to_datetime(timeline_df['date_start'])
        
        # Create daily view
        daily_counts = timeline_df.groupby(timeline_df['date_start'].dt.date).size().reset_index()
        daily_counts.columns = ['Date', 'Events']
        
        fig_timeline = px.bar(
            daily_counts,
            x='Date',
            y='Events',
            title='Daily Torch Relay Activity',
            color='Events',
            color_continuous_scale='Reds',
            height=300
        )
        
        fig_timeline.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of Events",
            showlegend=False
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Data table
    st.markdown("---")
    st.subheader("📋 Detailed Schedule")
    
    search_term = st.text_input("🔍 Search cities or events:")
    
    display_df = df_filtered.copy()
    if search_term:
        mask = (
            display_df['city'].astype(str).str.contains(search_term, case=False, na=False) |
            display_df['title'].astype(str).str.contains(search_term, case=False, na=False)
        )
        display_df = display_df[mask]
    
    st.dataframe(
        display_df[['stage_number', 'city', 'title', 'date_start', 'date_end', 'tag']],
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("📁 Please ensure the torch_route.csv file is in the project directory.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888; font-size: 0.9em;'>"
    "🔥 Paris 2024 Olympic Torch Relay Dashboard | Built with Streamlit & Plotly"
    "</div>",
    unsafe_allow_html=True
)