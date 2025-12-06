import streamlit as st
import pandas as pd
import numpy as np
import ast


athletes = pd.read_csv("data/athletes.csv")

st.title("Athletes")
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


    
    def get_athlete_image(name):
        return "https://img.olympics.com/images/image/private/t_1-1_300/f_auto/primary/pgotjrtojoadz7ylp7gv"

    athlete['disciplines'] = ast.literal_eval(athlete['disciplines'])
    athlete['events'] = ast.literal_eval(athlete['events'])
    athlete['image'] = get_athlete_image(athlete['name'])

    
    st.subheader("Selected Athlete Profile")

    col1, col2 = st.columns([1, 3], gap="large")

    with col1:
        if athlete["image"]:
            st.image(athlete["image"], width=160)
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


