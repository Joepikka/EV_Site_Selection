import os

import folium
import geopandas as gpd
import streamlit as st

from streamlit_folium import st_folium


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Thrissur EV Site Selection",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ AI-Powered GIS Decision Support System")

st.subheader(
    "EV Charging Station Site Selection — Thrissur District"
)

st.info(
    "Current Stage: EV distance calculation, "
    "EV candidate filtering, and road distance calculation completed."
)


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

BOUNDARY_FILE = "data/processed/thrissur_boundary.geojson"

GRID_FILE = "data/processed/thrissur_grid.geojson"

CANDIDATE_FILE = "data/processed/candidate_sites.geojson"

EV_DISTANCE_FILE = (
    "data/processed/candidate_sites_ev_distance.geojson"
)

FILTERED_FILE = (
    "data/processed/candidate_sites_filtered.geojson"
)

ROAD_DISTANCE_FILE = (
    "data/processed/candidate_sites_road_distance.geojson"
)

EV_STATIONS_FILE = (
    "data/raw/ev_stations/thrissur_ev_stations.geojson"
)

ROADS_FILE = "data/raw/roads/thrissur_roads.geojson"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_geojson(filepath):

    if os.path.exists(filepath):
        return gpd.read_file(filepath)

    return None


boundary = load_geojson(BOUNDARY_FILE)

grid = load_geojson(GRID_FILE)

candidate_sites = load_geojson(CANDIDATE_FILE)

ev_distance_sites = load_geojson(EV_DISTANCE_FILE)

filtered_sites = load_geojson(FILTERED_FILE)

road_distance_sites = load_geojson(ROAD_DISTANCE_FILE)

ev_stations = load_geojson(EV_STATIONS_FILE)

roads = load_geojson(ROADS_FILE)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Map Controls")


candidate_layer = st.sidebar.selectbox(

    "Candidate Sites Layer",

    [
        "Road Distance Results",
        "EV Filtered Sites",
        "All Candidate Sites"
    ]
)


show_boundary = st.sidebar.checkbox(
    "Show Thrissur Boundary",
    value=True
)


show_grid = st.sidebar.checkbox(
    "Show 1 km Grid",
    value=False
)


show_roads = st.sidebar.checkbox(
    "Show Road Network",
    value=False
)


show_ev_stations = st.sidebar.checkbox(
    "Show Existing EV Stations",
    value=True
)


show_candidates = st.sidebar.checkbox(
    "Show Candidate Sites",
    value=True
)


# --------------------------------------------------
# PROJECT PROGRESS
# --------------------------------------------------

st.subheader("📊 Project Progress")


progress_steps = [

    (
        "Thrissur Boundary Extraction",
        BOUNDARY_FILE
    ),

    (
        "1 km Candidate Grid Creation",
        GRID_FILE
    ),

    (
        "Existing EV Stations Download",
        EV_STATIONS_FILE
    ),

    (
        "EV Distance Calculation",
        EV_DISTANCE_FILE
    ),

    (
        "EV Distance Candidate Filtering",
        FILTERED_FILE
    ),

    (
        "Thrissur Road Network Download",
        ROADS_FILE
    ),

    (
        "Road Distance Calculation",
        ROAD_DISTANCE_FILE
    )
]


completed_steps = sum(

    os.path.exists(filepath)

    for _, filepath in progress_steps
)


total_steps = len(progress_steps)


st.progress(
    completed_steps / total_steps
)


st.write(

    f"Completed: {completed_steps}/{total_steps} GIS preprocessing steps"

)


for step_name, filepath in progress_steps:

    if os.path.exists(filepath):

        st.write(f"✅ {step_name}")

    else:

        st.write(f"⬜ {step_name}")


# --------------------------------------------------
# DATASET STATISTICS
# --------------------------------------------------

st.subheader("📈 Dataset Statistics")


column1, column2, column3, column4 = st.columns(4)


column1.metric(

    "Original Candidates",

    len(candidate_sites)
    if candidate_sites is not None
    else "N/A"

)


column2.metric(

    "Existing EV Stations",

    len(ev_stations)
    if ev_stations is not None
    else "N/A"

)


column3.metric(

    "After EV Filter",

    len(filtered_sites)
    if filtered_sites is not None
    else "N/A"

)


column4.metric(

    "Road Distance Results",

    len(road_distance_sites)
    if road_distance_sites is not None
    else "N/A"

)


# --------------------------------------------------
# DISTANCE STATISTICS
# --------------------------------------------------

st.subheader("📏 Distance Statistics")


distance_column1, distance_column2, distance_column3 = (
    st.columns(3)
)


if (
    road_distance_sites is not None
    and "nearest_ev_distance" in road_distance_sites.columns
):

    average_ev_distance = (
        road_distance_sites["nearest_ev_distance"].mean()
    )

    distance_column1.metric(

        "Average EV Distance",

        f"{average_ev_distance:.2f} m"

    )

else:

    distance_column1.metric(
        "Average EV Distance",
        "N/A"
    )


if (
    road_distance_sites is not None
    and "nearest_road_distance" in road_distance_sites.columns
):

    average_road_distance = (
        road_distance_sites["nearest_road_distance"].mean()
    )

    distance_column2.metric(

        "Average Road Distance",

        f"{average_road_distance:.2f} m"

    )

else:

    distance_column2.metric(
        "Average Road Distance",
        "N/A"
    )


if (
    road_distance_sites is not None
    and "nearest_road_distance" in road_distance_sites.columns
):

    minimum_road_distance = (
        road_distance_sites["nearest_road_distance"].min()
    )

    distance_column3.metric(

        "Minimum Road Distance",

        f"{minimum_road_distance:.2f} m"

    )

else:

    distance_column3.metric(
        "Minimum Road Distance",
        "N/A"
    )


# --------------------------------------------------
# SELECT DATASET FOR MAP
# --------------------------------------------------

if candidate_layer == "Road Distance Results":

    selected_sites = road_distance_sites


elif candidate_layer == "EV Filtered Sites":

    selected_sites = filtered_sites


else:

    selected_sites = candidate_sites


# --------------------------------------------------
# MAP CENTER
# --------------------------------------------------

if boundary is not None:

    boundary_wgs84 = boundary.to_crs(epsg=4326)

    center = boundary_wgs84.geometry.union_all().centroid

    map_center = [
        center.y,
        center.x
    ]

else:

    map_center = [
        10.5276,
        76.2144
    ]


# --------------------------------------------------
# CREATE MAP
# --------------------------------------------------

st.subheader("🗺️ Thrissur GIS Processing Map")


thrissur_map = folium.Map(

    location=map_center,

    zoom_start=10,

    tiles="OpenStreetMap"

)


# --------------------------------------------------
# BOUNDARY
# --------------------------------------------------

if show_boundary and boundary is not None:

    folium.GeoJson(

        boundary,

        name="Thrissur Boundary",

        style_function=lambda feature: {

            "color": "black",

            "weight": 3,

            "fillOpacity": 0

        }

    ).add_to(thrissur_map)


# --------------------------------------------------
# GRID
# --------------------------------------------------

if show_grid and grid is not None:

    folium.GeoJson(

        grid,

        name="1 km Grid",

        style_function=lambda feature: {

            "color": "blue",

            "weight": 0.5,

            "fillOpacity": 0.05

        }

    ).add_to(thrissur_map)


# --------------------------------------------------
# ROADS
# --------------------------------------------------

if show_roads and roads is not None:

    folium.GeoJson(

        roads,

        name="Road Network",

        style_function=lambda feature: {

            "color": "gray",

            "weight": 1

        }

    ).add_to(thrissur_map)


# --------------------------------------------------
# EXISTING EV STATIONS
# --------------------------------------------------

if show_ev_stations and ev_stations is not None:

    ev_stations = ev_stations.to_crs(epsg=4326)


    for _, station in ev_stations.iterrows():

        station_name = station.get(
            "name",
            "Existing EV Station"
        )


        folium.Marker(

            location=[

                station.geometry.y,

                station.geometry.x

            ],

            popup=(

                "<b>Existing EV Station</b><br>"

                f"{station_name}"

            ),

            tooltip="Existing EV Station",

            icon=folium.Icon(

                color="green",

                icon="bolt",

                prefix="fa"

            )

        ).add_to(thrissur_map)


# --------------------------------------------------
# CANDIDATE SITES
# --------------------------------------------------

if show_candidates and selected_sites is not None:

    selected_sites = selected_sites.to_crs(epsg=4326)


    for _, site in selected_sites.iterrows():

        latitude = site.geometry.y

        longitude = site.geometry.x


        popup_lines = [

            "<b>Candidate EV Site</b>",

            f"Latitude: {latitude:.6f}",

            f"Longitude: {longitude:.6f}"

        ]


        if "nearest_ev_distance" in selected_sites.columns:

            popup_lines.append(

                "Nearest Existing EV Station: "

                f"{site['nearest_ev_distance']:.2f} m"

            )


        if "nearest_road_distance" in selected_sites.columns:

            popup_lines.append(

                "Nearest Road: "

                f"{site['nearest_road_distance']:.2f} m"

            )


        popup_text = "<br>".join(popup_lines)


        folium.CircleMarker(

            location=[
                latitude,
                longitude
            ],

            radius=3,

            popup=popup_text,

            tooltip="Candidate EV Site",

            weight=1,

            fill=True,

            fill_opacity=0.8

        ).add_to(thrissur_map)


# --------------------------------------------------
# MAP DISPLAY
# --------------------------------------------------

folium.LayerControl().add_to(thrissur_map)


st_folium(

    thrissur_map,

    width=1200,

    height=650

)


# --------------------------------------------------
# RESULTS TABLE
# --------------------------------------------------

st.subheader("📋 Latest GIS Processing Results")


if road_distance_sites is not None:

    display_columns = [

        column

        for column in [

            "site_id",

            "latitude",

            "longitude",

            "nearest_ev_distance",

            "nearest_road_distance"

        ]

        if column in road_distance_sites.columns

    ]


    st.dataframe(

        road_distance_sites[display_columns],

        use_container_width=True,

        hide_index=True

    )


else:

    st.warning(

        "candidate_sites_road_distance.geojson not found."

    )


# --------------------------------------------------
# NEXT STEPS
# --------------------------------------------------

st.subheader("🚀 Remaining Project Steps")


st.write("⬜ Add Population Density")

st.write("⬜ Add Terrain Slope")

st.write("⬜ Add Flood Hazard")

st.write("⬜ Add Commercial Activity Score")

st.write("⬜ Perform MCDA Suitability Analysis")

st.write("⬜ Train Random Forest Model")

st.write("⬜ Generate Final EV Charging Station Recommendations")