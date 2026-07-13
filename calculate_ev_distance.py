import os
import geopandas as gpd


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

candidate_file = "data/processed/candidate_sites.geojson"

ev_file = "data/raw/ev_stations/thrissur_ev_stations.geojson"

output_file = "data/processed/candidate_sites_ev_distance.geojson"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("Reading candidate sites...")

candidates = gpd.read_file(candidate_file)

print("Candidate sites:", len(candidates))


print("Reading EV charging stations...")

ev_stations = gpd.read_file(ev_file)

print("EV charging stations:", len(ev_stations))


# --------------------------------------------------
# CHECK FOR EMPTY DATA
# --------------------------------------------------

if candidates.empty:
    raise ValueError("Candidate sites dataset is empty.")

if ev_stations.empty:
    raise ValueError("EV charging stations dataset is empty.")


# --------------------------------------------------
# CONVERT TO METRIC CRS
# EPSG:32643 = UTM Zone 43N
# Distance calculations will be in meters
# --------------------------------------------------

print("Converting data to metric CRS...")

candidates_metric = candidates.to_crs(epsg=32643)

ev_stations_metric = ev_stations.to_crs(epsg=32643)


# --------------------------------------------------
# FIND NEAREST EV CHARGING STATION
# --------------------------------------------------

print("Calculating distance to nearest EV charging station...")

nearest = gpd.sjoin_nearest(
    candidates_metric,
    ev_stations_metric[["ocm_id", "name", "geometry"]],
    how="left",
    distance_col="nearest_ev_distance"
)


# --------------------------------------------------
# HANDLE POSSIBLE EQUAL-DISTANCE DUPLICATES
# --------------------------------------------------

nearest = nearest[
    ~nearest.index.duplicated(keep="first")
].copy()


# --------------------------------------------------
# CLEAN COLUMNS
# --------------------------------------------------

nearest = nearest.rename(
    columns={
        "ocm_id": "nearest_ev_id",
        "name": "nearest_ev_name"
    }
)

nearest = nearest.drop(
    columns=["index_right"],
    errors="ignore"
)


# --------------------------------------------------
# CONVERT BACK TO WGS84
# --------------------------------------------------

print("Converting results back to EPSG:4326...")

nearest = nearest.to_crs(epsg=4326)


# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

nearest.to_file(
    output_file,
    driver="GeoJSON"
)


# --------------------------------------------------
# PRINT RESULTS
# --------------------------------------------------

print("----------------------------------")
print("SUCCESS")
print("----------------------------------")

print("Candidate sites processed:", len(nearest))

print(
    "Minimum nearest EV distance:",
    round(nearest["nearest_ev_distance"].min(), 2),
    "meters"
)

print(
    "Average nearest EV distance:",
    round(nearest["nearest_ev_distance"].mean(), 2),
    "meters"
)

print(
    "Maximum nearest EV distance:",
    round(nearest["nearest_ev_distance"].max(), 2),
    "meters"
)

print("Saved to:", output_file)