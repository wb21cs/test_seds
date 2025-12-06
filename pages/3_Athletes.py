import streamlit as st
import pandas as pd
import numpy as np

athletes = pd.read_csv("data/athletes.csv")
st.write(str(np.array(athletes.loc[athletes["code"] == 1532872, "name"])[0]))

st.title("Athletes")
selected_athlete = st.selectbox(label="Select an athlete:",
             options=athletes["code"],
             index=None,
             placeholder="Choose an athlete...",
             format_func=lambda opt: str(np.array(athletes.loc[athletes["code"] == opt, "name"])[0])
             )
selected_athlete


st.subheader("Selected Athlete Profile")

# --- PLACEHOLDER DATA (replace later with real values) ---
athlete = {
    "name": "Select an athlete",
    "country": "N/A",
    "height": "—",
    "weight": "—",
    "sports": "—",
    "disciplines": "—",
    "coaches": "—",
    "image": None  # or a placeholder image URL later
}

# --- PROFILE CARD LAYOUT ---
col1, col2 = st.columns([1, 3], gap="large")

with col1:
    st.image("https://img.olympics.com/images/image/private/t_1-1_300/f_auto/primary/pgotjrtojoadz7ylp7gv", width=160)
    # if athlete["image"]:
    #     st.image(athlete["image"], width=160)
    # else:
    #     st.markdown(
    #         """
    #         <div style="
    #             width:160px;
    #             height:160px;
    #             border-radius:50%;
    #             background:#e5e7eb;
    #             display:flex;
    #             align-items:center;
    #             justify-content:center;
    #             font-size:48px;
    #             color:#6b7280;">
    #             👤
    #         </div>
    #         """,
    #         unsafe_allow_html=True
    #     )

with col2:
    st.markdown(f"### {athlete['name']}")
    st.markdown(f"**Country / NOC:** {athlete['country']}")
    st.markdown(f"**Height:** {athlete['height']} cm")
    st.markdown(f"**Weight:** {athlete['weight']} kg")
    st.markdown(f"**Sport(s):** {athlete['sports']}")
    st.markdown(f"**Discipline(s):** {athlete['disciplines']}")
    st.markdown(f"**Coach(s):** {athlete['coaches']}")