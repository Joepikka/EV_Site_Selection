import os
import requests
import geopandas as gpd
from shapely.geometry import Point
import streamlit as st


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

boundary_file = "data/processed/thrissur_boundary.geojson"

output_folder = "data/raw/ev_stations"

output_file = os.path.join(
    output_folder,
    "thrissur_ev_stations.geojson"
)


# --------------------------------------------------
# READ API KEY
# --------------------------------------------------

API_KEY = st.secrets["OPENCHARGEMAP_API_KEY"]


# --------------------------------------------------
# READ THRISSUR BOUNDARY
# --------------------------------------------------

print("Reading Thrissur boundary...")

boundary = gpd.read_file(boundary_file)

boundary = boundary.to_crs(epsg=4326)


# --------------------------------------------------
# GET THRISSUR BOUNDING BOX
# --------------------------------------------------

min_lon, min_lat, max_lon, max_lat = boundary.total_bounds

bounding_box = (
    f"({min_lat},{min_lon}),"
    f"({max_lat},{max_lon})"
)

print("Bounding box:", bounding_box)


# --------------------------------------------------
# OPEN CHARGE MAP API
# --------------------------------------------------

url = "https://api.openchargemap.io/v3/poi/"

params = {
    "output": "json",

    "boundingbox": bounding_box,

    "maxresults": 1000,

    "compact": True,

    "verbose": False,

    "key": API_KEY
}


# --------------------------------------------------
# DOWNLOAD DATA
# --------------------------------------------------

print("Downloading EV charging stations from Open Charge Map...")

response = requests.get(
    url,
    params=params,
    timeout=60
)

response.raise_for_status()

data = response.json()

print("Objects returned by Open Charge Map:", len(data))


# --------------------------------------------------
# CONVERT TO GEODATAFRAME
# --------------------------------------------------

records = []

for station in data:

    address = station.get("AddressInfo", {})

    latitude = address.get("Latitude")
    longitude = address.get("Longitude")

    if latitude is None or longitude is None:
        continue

    records.append({

        "ocm_id": station.get("ID"),

        "name": address.get("Title"),

        "address": address.get("AddressLine1"),

        "town": address.get("Town"),

        "postcode": address.get("Postcode"),

        "latitude": latitude,

        "longitude": longitude,

        "geometry": Point(
            longitude,
            latitude
        )
    })


stations = gpd.GeoDataFrame(
    records,
    geometry="geometry",
    crs="EPSG:4326"
)


# --------------------------------------------------
# KEEP ONLY STATIONS INSIDE THRISSUR
# --------------------------------------------------

if not stations.empty:

    stations = gpd.sjoin(
        stations,
        boundary[["geometry"]],
        predicate="within",
        how="inner"
    )

    stations = stations.drop(
        columns=["index_right"],
        errors="ignore"
    )


# --------------------------------------------------
# SAVE DATA
# --------------------------------------------------

os.makedirs(
    output_folder,
    exist_ok=True
)

stations.to_file(
    output_file,
    driver="GeoJSON"
)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("----------------------------------")
print("SUCCESS")
print("----------------------------------")

print(
    "Number of EV charging stations:",
    len(stations)
)

print(
    "Saved to:",
    output_file
)

print(
    "CRS:",
    stations.crs
)