import joblib
import pandas as pd
import streamlit as st
import folium

from streamlit_folium import st_folium


# --------------------------------
# PAGE SETTINGS
# --------------------------------

st.set_page_config(
    page_title="Kerala EV Site Selection",
    page_icon="⚡",
    layout="wide"
)


st.title("AI-Powered GIS Decision Support System")

st.subheader("EV Charging Station Site Selection")


# --------------------------------
# LOAD DATA
# --------------------------------

@st.cache_data
def load_data():

    return pd.read_csv(
        "data/ev_sites_scored.csv"
    )


@st.cache_resource
def load_model():

    return joblib.load(
        "models/ev_random_forest.pkl"
    )


data = load_data()

model = load_model()


# --------------------------------
# ML FEATURES
# --------------------------------

FEATURES = [
    "road_distance",
    "population_density",
    "existing_charger_distance",
    "slope",
    "flood_hazard",
    "commercial_score"
]


# --------------------------------
# ML PREDICTION
# --------------------------------

data["ml_prediction"] = model.predict(
    data[FEATURES]
)


# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.header("Site Selection Controls")


minimum_score = st.sidebar.slider(
    "Minimum Suitability Score",
    min_value=0,
    max_value=100,
    value=70
)


number_of_sites = st.sidebar.slider(
    "Number of Recommended Sites",
    min_value=5,
    max_value=100,
    value=20
)


# --------------------------------
# FILTER AND RANK SITES
# --------------------------------

recommended_sites = (

    data[
        data["suitability_score"]
        >= minimum_score
    ]

    .sort_values(
        "suitability_score",
        ascending=False
    )

    .head(number_of_sites)

)


# --------------------------------
# DASHBOARD METRICS
# --------------------------------

column1, column2, column3 = st.columns(3)


column1.metric(
    "Total Candidate Sites",
    len(data)
)


column2.metric(
    "Suitable Sites",
    len(
        data[
            data["suitability_score"]
            >= minimum_score
        ]
    )
)


column3.metric(
    "Displayed Recommendations",
    len(recommended_sites)
)


# --------------------------------
# INTERACTIVE MAP
# --------------------------------

st.subheader(
    "Recommended EV Charging Station Locations"
)


kerala_map = folium.Map(

    location=[
        10.5,
        76.2
    ],

    zoom_start=7
)


for _, site in recommended_sites.iterrows():

    popup_text = f"""

    <b>Suitability Score:</b>
    {site['suitability_score']:.2f}

    <br>

    <b>Population Density:</b>
    {site['population_density']:.0f}

    <br>

    <b>Road Distance:</b>
    {site['road_distance']:.2f} km

    <br>

    <b>Slope:</b>
    {site['slope']:.2f} degrees

    <br>

    <b>Flood Hazard:</b>
    {site['flood_hazard']:.2f}

    <br>

    <b>ML Prediction:</b>
    {int(site['ml_prediction'])}

    """


    folium.Marker(

        location=[
            site["latitude"],
            site["longitude"]
        ],

        popup=popup_text,

        tooltip=(
            f"Suitability Score: "
            f"{site['suitability_score']:.2f}"
        ),

        icon=folium.Icon(
            icon="bolt",
            prefix="fa"
        )

    ).add_to(kerala_map)


st_folium(
    kerala_map,
    width=1200,
    height=600
)


# --------------------------------
# RESULTS TABLE
# --------------------------------

st.subheader("Top Recommended Sites")


st.dataframe(

    recommended_sites[

        [
            "latitude",
            "longitude",
            "suitability_score",
            "ml_prediction",
            "road_distance",
            "population_density",
            "existing_charger_distance",
            "slope",
            "flood_hazard",
            "commercial_score"
        ]

    ],

    use_container_width=True

)