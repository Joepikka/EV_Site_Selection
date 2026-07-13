import os
import geopandas as gpd


# --------------------------------------------------
# FILE PATHS
# --------------------------------------------------

candidate_file = "data/processed/candidate_sites_filtered.geojson"

road_file = "data/raw/roads/thrissur_roads.geojson"

output_file = "data/processed/candidate_sites_road_distance.geojson"


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

print("Reading filtered candidate sites...")

candidates = gpd.read_file(candidate_file)

print("Candidate sites:", len(candidates))


print("Reading Thrissur roads...")

roads = gpd.read_file(road_file)

print("Road segments:", len(roads))


# --------------------------------------------------
# CHECK EMPTY DATASETS
# --------------------------------------------------

if candidates.empty:
    raise ValueError("Candidate sites dataset is empty.")

if roads.empty:
    raise ValueError("Road dataset is empty.")


# --------------------------------------------------
# CONVERT TO METRIC CRS
#
# EPSG:32643 = UTM Zone 43N
# Distances will be calculated in meters
# --------------------------------------------------

print("Converting datasets to metric CRS...")

candidates_metric = candidates.to_crs(epsg=32643)

roads_metric = roads.to_crs(epsg=32643)


# --------------------------------------------------
# FIND NEAREST ROAD
# --------------------------------------------------

print("Calculating distance to nearest road...")

nearest = gpd.sjoin_nearest(
    candidates_metric,
    roads_metric[["geometry"]],
    how="left",
    distance_col="nearest_road_distance"
)


# --------------------------------------------------
# REMOVE POSSIBLE DUPLICATES
# --------------------------------------------------

nearest = nearest[
    ~nearest.index.duplicated(keep="first")
].copy()


# --------------------------------------------------
# REMOVE JOIN COLUMN
# --------------------------------------------------

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
# SAVE OUTPUT
# --------------------------------------------------

os.makedirs("data/processed", exist_ok=True)

nearest.to_file(
    output_file,
    driver="GeoJSON"
)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print("----------------------------------")
print("SUCCESS")
print("----------------------------------")

print("Candidate sites processed:", len(nearest))

print(
    "Minimum nearest road distance:",
    round(nearest["nearest_road_distance"].min(), 2),
    "meters"
)

print(
    "Average nearest road distance:",
    round(nearest["nearest_road_distance"].mean(), 2),
    "meters"
)

print(
    "Maximum nearest road distance:",
    round(nearest["nearest_road_distance"].max(), 2),
    "meters"
)

print("Saved to:", output_file)