import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Sports & Events - Paris 2024",
    page_icon="🏟️",
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
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    /* Override Streamlit's metric styling for better contrast */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
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
st.markdown('<p class="main-header">🏟️ Sports & Events Arena</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Explore the competitive landscape of Paris 2024 Olympics</p>', unsafe_allow_html=True)

# Load data with error handling
@st.cache_data
def load_data():
    try:
        events = pd.read_csv('data/events.csv')
        schedules = pd.read_csv('data/schedules.csv')
        venues = pd.read_csv('data/venues.csv')
        medals = pd.read_csv('data/medals.csv')
        athletes = pd.read_csv('data/athletes.csv')
        nocs = pd.read_csv('data/nocs.csv')
        
        return events, schedules, venues, medals, athletes, nocs
    except FileNotFoundError as e:
        st.error(f"⚠️ Error loading data: {e}")
        st.info("Please ensure all CSV files are in the 'data/' directory.")
        return None, None, None, None, None, None

events, schedules, venues, medals, athletes, nocs = load_data()

if events is None:
    st.stop()

# Sidebar filters
st.sidebar.header("🎯 Global Filters")

# Country filter
if 'country' in nocs.columns:
    countries = sorted(nocs['country'].dropna().unique())
    selected_countries = st.sidebar.multiselect("🌍 Select Countries", countries, default=[])
else:
    selected_countries = []

# Sport filter
if 'sport' in events.columns:
    sports = sorted(events['sport'].dropna().unique())
    selected_sports = st.sidebar.multiselect("🏅 Select Sports", sports, default=[])
else:
    selected_sports = []

# Medal type filter
st.sidebar.subheader("🥇 Medal Types")
show_gold = st.sidebar.checkbox("Gold", value=True)
show_silver = st.sidebar.checkbox("Silver", value=True)
show_bronze = st.sidebar.checkbox("Bronze", value=True)

# Venue filter (creative addition)
if 'venue' in venues.columns:
    venue_list = sorted(venues['venue'].dropna().unique())
    selected_venues = st.sidebar.multiselect("🏛️ Select Venues", venue_list, default=[])
else:
    selected_venues = []

# Discipline filter (creative addition)
if 'discipline' in schedules.columns:
    disciplines = sorted(schedules['discipline'].dropna().unique())
    selected_disciplines = st.sidebar.multiselect("🎯 Select Disciplines", disciplines, default=[])
else:
    selected_disciplines = []

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Use filters to customize your view!")

# Filter data based on selections
filtered_events = events.copy()
filtered_medals = medals.copy()
filtered_schedules = schedules.copy()

if selected_sports:
    filtered_events = filtered_events[filtered_events['sport'].isin(selected_sports)]
    if 'discipline' in filtered_medals.columns:
        # Map disciplines to sports (if needed)
        filtered_medals = filtered_medals[filtered_medals['discipline'].isin(selected_sports)]

if selected_disciplines:
    if 'discipline' in filtered_schedules.columns:
        filtered_schedules = filtered_schedules[filtered_schedules['discipline'].isin(selected_disciplines)]
    if 'discipline' in filtered_medals.columns:
        filtered_medals = filtered_medals[filtered_medals['discipline'].isin(selected_disciplines)]

if selected_countries and 'country_code' in filtered_medals.columns:
    country_codes = nocs[nocs['country'].isin(selected_countries)]['code'].values
    filtered_medals = filtered_medals[filtered_medals['country_code'].isin(country_codes)]

if selected_venues:
    if 'venue' in filtered_schedules.columns:
        filtered_schedules = filtered_schedules[filtered_schedules['venue'].isin(selected_venues)]

# Filter by medal type
medal_types = []
if show_gold: medal_types.append('Gold Medal')
if show_silver: medal_types.append('Silver Medal')
if show_bronze: medal_types.append('Bronze Medal')

if medal_types and 'medal_type' in filtered_medals.columns:
    filtered_medals = filtered_medals[filtered_medals['medal_type'].isin(medal_types)]

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sports = filtered_events['sport'].nunique() if 'sport' in filtered_events.columns else 0
    st.metric("🏅 Total Sports", total_sports)

with col2:
    total_events = len(filtered_events)
    st.metric("🎯 Total Events", total_events)

with col3:
    total_venues = venues['venue'].nunique() if 'venue' in venues.columns else 0
    st.metric("🏛️ Venues", total_venues)

with col4:
    total_medals_awarded = len(filtered_medals)
    st.metric("🏆 Medals Awarded", total_medals_awarded)

st.markdown("---")

# Main content tabs
tab1, tab2, tab3, tab4 = st.tabs(["📅 Event Schedule", "🏆 Medal Analysis", "🗺️ Venue Map", "🎨 Sport Insights"])

# TAB 1: EVENT SCHEDULE
with tab1:
    st.subheader("📅 Event Schedule Timeline")
    
    # Discipline selector for schedule
    if 'discipline' in filtered_schedules.columns:
        schedule_disciplines = sorted(filtered_schedules['discipline'].dropna().unique())
        
        if schedule_disciplines:
            selected_schedule_discipline = st.selectbox(
                "Select Discipline for Schedule View", 
                schedule_disciplines, 
                key="schedule_discipline"
            )
            
            # Filter schedule by discipline
            discipline_schedule = filtered_schedules[
                filtered_schedules['discipline'] == selected_schedule_discipline
            ].copy()
            
            if not discipline_schedule.empty and 'start_date' in discipline_schedule.columns:
                # Parse dates
                discipline_schedule['start_date'] = pd.to_datetime(
                    discipline_schedule['start_date'], 
                    errors='coerce'
                )
                
                if 'end_date' in discipline_schedule.columns:
                    discipline_schedule['end_date'] = pd.to_datetime(
                        discipline_schedule['end_date'], 
                        errors='coerce'
                    )
                else:
                    discipline_schedule['end_date'] = discipline_schedule['start_date']
                
                # Remove rows with invalid dates
                discipline_schedule = discipline_schedule.dropna(subset=['start_date'])
                discipline_schedule['end_date'] = discipline_schedule['end_date'].fillna(
                    discipline_schedule['start_date']
                )
                
                if not discipline_schedule.empty:
                    # Create event label
                    if 'event' in discipline_schedule.columns:
                        discipline_schedule['event_label'] = discipline_schedule['event']
                    elif 'phase' in discipline_schedule.columns:
                        discipline_schedule['event_label'] = discipline_schedule['phase']
                    else:
                        discipline_schedule['event_label'] = 'Event ' + discipline_schedule.index.astype(str)
                    
                    # Create Gantt chart
                    fig_gantt = px.timeline(
                        discipline_schedule.head(50),  # Limit to 50 events for readability
                        x_start='start_date',
                        x_end='end_date',
                        y='event_label',
                        color='venue' if 'venue' in discipline_schedule.columns else 'gender',
                        title=f"Event Schedule for {selected_schedule_discipline}",
                        labels={'event_label': 'Event'},
                        height=max(500, min(len(discipline_schedule) * 25, 1000))
                    )
                    
                    fig_gantt.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Event",
                        showlegend=True,
                        hovermode='closest'
                    )
                    
                    st.plotly_chart(fig_gantt, use_container_width=True)
                    
                    # Event statistics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("📊 Total Events", len(discipline_schedule))
                    
                    with col2:
                        if 'gender' in discipline_schedule.columns:
                            gender_dist = discipline_schedule['gender'].value_counts()
                            st.metric("🚹 Men's Events", gender_dist.get('M', 0))
                    
                    with col3:
                        if 'gender' in discipline_schedule.columns:
                            st.metric("🚺 Women's Events", gender_dist.get('W', 0))
                    
                    # Event details table
                    with st.expander("📋 View Detailed Schedule"):
                        display_cols = ['event', 'start_date', 'end_date', 'venue', 'gender', 'phase']
                        available_cols = [col for col in display_cols if col in discipline_schedule.columns]
                        st.dataframe(
                            discipline_schedule[available_cols].sort_values('start_date'), 
                            use_container_width=True,
                            hide_index=True
                        )
                else:
                    st.warning("⚠️ No valid schedule data available for this discipline.")
            else:
                st.warning("⚠️ Schedule data not available for this discipline.")
        else:
            st.info("📅 No disciplines available with current filters.")
    else:
        st.warning("⚠️ Schedule data not properly formatted.")

# TAB 2: MEDAL ANALYSIS
with tab2:
    st.subheader("🏆 Medal Distribution by Sport")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Treemap of medals by sport/discipline
        if not filtered_medals.empty and 'discipline' in filtered_medals.columns:
            # Create medal hierarchy
            medal_hierarchy = filtered_medals.groupby(['discipline', 'medal_type']).size().reset_index(name='count')
            
            # Clean medal types for display
            medal_hierarchy['medal_display'] = medal_hierarchy['medal_type'].str.replace(' Medal', '')
            
            fig_treemap = px.treemap(
                medal_hierarchy,
                path=['discipline', 'medal_display'],
                values='count',
                color='count',
                color_continuous_scale='Viridis',
                title="Medal Count by Discipline (Treemap)"
            )
            
            fig_treemap.update_traces(textinfo="label+value+percent parent")
            fig_treemap.update_layout(height=600)
            
            st.plotly_chart(fig_treemap, use_container_width=True)
    
    with col2:
        # Top disciplines by medals
        if not filtered_medals.empty and 'discipline' in filtered_medals.columns:
            top_disciplines = filtered_medals['discipline'].value_counts().head(10)
            
            fig_top_disciplines = go.Figure(data=[
                go.Bar(
                    y=top_disciplines.index,
                    x=top_disciplines.values,
                    orientation='h',
                    marker=dict(
                        color=top_disciplines.values,
                        colorscale='Blues',
                        showscale=True
                    ),
                    text=top_disciplines.values,
                    textposition='auto'
                )
            ])
            
            fig_top_disciplines.update_layout(
                title="Top 10 Disciplines by Medal Count",
                xaxis_title="Number of Medals",
                yaxis_title="Discipline",
                height=600
            )
            
            st.plotly_chart(fig_top_disciplines, use_container_width=True)
    
    # Medal type distribution pie chart
    st.markdown("### 🥇 Medal Type Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if not filtered_medals.empty and 'medal_type' in filtered_medals.columns:
            medal_type_dist = filtered_medals['medal_type'].value_counts()
            
            # Map medal types to colors
            color_map = {
                'Gold Medal': '#FFD700',
                'Silver Medal': '#C0C0C0',
                'Bronze Medal': '#CD7F32'
            }
            colors = [color_map.get(medal, '#CCCCCC') for medal in medal_type_dist.index]
            
            fig_medal_pie = go.Figure(data=[go.Pie(
                labels=medal_type_dist.index,
                values=medal_type_dist.values,
                marker=dict(colors=colors),
                hole=0.4
            )])
            
            fig_medal_pie.update_layout(title="Distribution of Medal Types")
            
            st.plotly_chart(fig_medal_pie, use_container_width=True)
    
    with col2:
        # Gender distribution in medals
        if not filtered_medals.empty and 'gender' in filtered_medals.columns:
            gender_dist = filtered_medals['gender'].value_counts()
            
            fig_gender = px.pie(
                values=gender_dist.values,
                names=gender_dist.index,
                title="Medal Distribution by Gender",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            st.plotly_chart(fig_gender, use_container_width=True)

# TAB 3: VENUE MAP
with tab3:
    st.subheader("🗺️ Olympic Venues in Paris")
    
    # Check if venues has the data we need
    if not venues.empty:
        # Display venue information
        st.markdown("### 🏛️ Olympic Venues Overview")
        
        # Venue statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📍 Total Venues", len(venues))
        
        with col2:
            if 'sports' in venues.columns:
                total_sports_venues = venues['sports'].str.split(',').apply(len).sum()
                st.metric("🏅 Sport-Venue Combinations", int(total_sports_venues))
        
        with col3:
            if 'date_start' in venues.columns and 'date_end' in venues.columns:
                venues['date_start'] = pd.to_datetime(venues['date_start'], errors='coerce')
                venues['date_end'] = pd.to_datetime(venues['date_end'], errors='coerce')
                venues['duration'] = (venues['date_end'] - venues['date_start']).dt.days
                avg_duration = venues['duration'].mean()
                st.metric("📅 Avg Venue Usage (days)", f"{avg_duration:.1f}")
        
        # Venue list with details
        st.markdown("### 📋 Venue Details")
        
        display_venues = venues.copy()
        if selected_venues:
            display_venues = display_venues[display_venues['venue'].isin(selected_venues)]
        
        # Count events per venue from schedules
        if 'venue' in schedules.columns:
            venue_event_counts = schedules['venue'].value_counts().reset_index()
            venue_event_counts.columns = ['venue', 'event_count']
            display_venues = display_venues.merge(venue_event_counts, on='venue', how='left')
            display_venues['event_count'] = display_venues['event_count'].fillna(0).astype(int)
        
        # Create interactive venue chart
        if 'sports' in display_venues.columns:
            # Split sports and create individual rows
            venue_sports_list = []
            for _, row in display_venues.iterrows():
                if pd.notna(row['sports']):
                    sports_list = [s.strip() for s in str(row['sports']).split(',')]
                    for sport in sports_list:
                        venue_sports_list.append({
                            'venue': row['venue'],
                            'sport': sport
                        })
            
            if venue_sports_list:
                venue_sports_df = pd.DataFrame(venue_sports_list)
                
                # Count sports per venue
                sports_per_venue = venue_sports_df.groupby('venue').size().reset_index(name='sport_count')
                
                fig_venue_sports = px.bar(
                    sports_per_venue.sort_values('sport_count', ascending=True).tail(15),
                    y='venue',
                    x='sport_count',
                    orientation='h',
                    title="Number of Sports per Venue (Top 15)",
                    labels={'sport_count': 'Number of Sports', 'venue': 'Venue'},
                    color='sport_count',
                    color_continuous_scale='Viridis'
                )
                
                fig_venue_sports.update_layout(height=500, showlegend=False)
                st.plotly_chart(fig_venue_sports, use_container_width=True)
        
        # Venue timeline
        if 'date_start' in venues.columns and 'date_end' in venues.columns:
            st.markdown("### 📅 Venue Usage Timeline")
            
            timeline_venues = venues.dropna(subset=['date_start', 'date_end']).copy()
            
            if not timeline_venues.empty:
                fig_venue_timeline = px.timeline(
                    timeline_venues.head(20),
                    x_start='date_start',
                    x_end='date_end',
                    y='venue',
                    title="Venue Usage Timeline",
                    labels={'venue': 'Venue'},
                    height=max(400, len(timeline_venues.head(20)) * 30)
                )
                
                fig_venue_timeline.update_layout(xaxis_title="Date")
                st.plotly_chart(fig_venue_timeline, use_container_width=True)
        
        # Detailed venue table
        with st.expander("📊 View Complete Venue Data"):
            display_cols = ['venue', 'sports', 'date_start', 'date_end']
            if 'event_count' in display_venues.columns:
                display_cols.append('event_count')
            available_cols = [col for col in display_cols if col in display_venues.columns]
            st.dataframe(display_venues[available_cols], use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Venue data not available.")

# TAB 4: SPORT INSIGHTS (Creative Addition)
with tab4:
    st.subheader("🎨 Deep Dive into Sport Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Events per Sport")
        if 'sport' in filtered_events.columns:
            events_per_sport = filtered_events['sport'].value_counts().reset_index()
            events_per_sport.columns = ['sport', 'count']
            
            fig_events = px.bar(
                events_per_sport.head(15),
                x='count',
                y='sport',
                orientation='h',
                title="Number of Events by Sport (Top 15)",
                color='count',
                color_continuous_scale='Plasma',
                text='count'
            )
            fig_events.update_traces(textposition='auto')
            fig_events.update_layout(showlegend=False, height=500)
            st.plotly_chart(fig_events, use_container_width=True)
    
    with col2:
        st.markdown("### 👥 Athlete Participation by Discipline")
        if 'disciplines' in athletes.columns:
            # Split disciplines and count
            discipline_list = []
            for disciplines_str in athletes['disciplines'].dropna():
                disciplines = [d.strip() for d in str(disciplines_str).split(',')]
                discipline_list.extend(disciplines)
            
            if discipline_list:
                discipline_counts = pd.Series(discipline_list).value_counts().reset_index()
                discipline_counts.columns = ['discipline', 'athletes']
                
                fig_athletes = px.bar(
                    discipline_counts.head(15),
                    x='athletes',
                    y='discipline',
                    orientation='h',
                    title="Number of Athletes by Discipline (Top 15)",
                    color='athletes',
                    color_continuous_scale='Viridis',
                    text='athletes'
                )
                fig_athletes.update_traces(textposition='auto')
                fig_athletes.update_layout(showlegend=False, height=500)
                st.plotly_chart(fig_athletes, use_container_width=True)
    
    # Medal timeline
    st.markdown("### 📅 Medal Awards Timeline")
    if 'medal_date' in filtered_medals.columns:
        filtered_medals['medal_date'] = pd.to_datetime(filtered_medals['medal_date'], errors='coerce')
        medals_by_date = filtered_medals.dropna(subset=['medal_date']).groupby('medal_date').size().reset_index(name='count')
        
        fig_timeline = px.line(
            medals_by_date,
            x='medal_date',
            y='count',
            title="Medals Awarded Over Time",
            labels={'medal_date': 'Date', 'count': 'Number of Medals'},
            markers=True
        )
        
        fig_timeline.update_layout(height=400)
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Sport comparison
    st.markdown("### 📊 Sport/Discipline Comparison Dashboard")
    
    if not filtered_medals.empty and 'discipline' in filtered_medals.columns:
        selected_disciplines_compare = st.multiselect(
            "Select disciplines to compare (up to 5)",
            sorted(filtered_medals['discipline'].unique()),
            max_selections=5,
            default=list(filtered_medals['discipline'].unique()[:3]) if len(filtered_medals['discipline'].unique()) >= 3 else []
        )
        
        if selected_disciplines_compare:
            comparison_data = []
            for discipline in selected_disciplines_compare:
                discipline_medals = filtered_medals[filtered_medals['discipline'] == discipline]
                comparison_data.append({
                    'Discipline': discipline,
                    'Gold': len(discipline_medals[discipline_medals['medal_type'] == 'Gold Medal']),
                    'Silver': len(discipline_medals[discipline_medals['medal_type'] == 'Silver Medal']),
                    'Bronze': len(discipline_medals[discipline_medals['medal_type'] == 'Bronze Medal']),
                    'Total': len(discipline_medals)
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            
            # Create grouped bar chart
            fig_compare = go.Figure()
            fig_compare.add_trace(go.Bar(
                name='Gold', 
                x=comparison_df['Discipline'], 
                y=comparison_df['Gold'], 
                marker_color='#FFD700',
                text=comparison_df['Gold'],
                textposition='auto'
            ))
            fig_compare.add_trace(go.Bar(
                name='Silver', 
                x=comparison_df['Discipline'], 
                y=comparison_df['Silver'], 
                marker_color='#C0C0C0',
                text=comparison_df['Silver'],
                textposition='auto'
            ))
            fig_compare.add_trace(go.Bar(
                name='Bronze', 
                x=comparison_df['Discipline'], 
                y=comparison_df['Bronze'], 
                marker_color='#CD7F32',
                text=comparison_df['Bronze'],
                textposition='auto'
            ))
            
            fig_compare.update_layout(
                title="Medal Comparison Across Disciplines",
                xaxis_title="Discipline",
                yaxis_title="Number of Medals",
                barmode='group',
                height=450
            )
            
            st.plotly_chart(fig_compare, use_container_width=True)
            
            # Comparison table
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🏟️ <strong>Paris 2024 Olympics - Sports & Events Analysis</strong></p>
    <p>Built with ❤️ using Streamlit | Data powered by competitive spirit</p>
</div>
""", unsafe_allow_html=True)