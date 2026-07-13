import os
import geopandas as gpd


input_file = "data/processed/candidate_sites_ev_distance.geojson"

output_file = "data/processed/candidate_sites_filtered.geojson"

MIN_EV_DISTANCE = 1000  # meters


print("Reading candidate sites...")

sites = gpd.read_file(input_file)

print("Original candidate sites:", len(sites))


# Remove candidates too close to existing EV stations

filtered_sites = sites[
    sites["nearest_ev_distance"] >= MIN_EV_DISTANCE
].copy()


# Reset index

filtered_sites = filtered_sites.reset_index(drop=True)


# Add a new site ID

filtered_sites["site_id"] = range(1, len(filtered_sites) + 1)


# Save

os.makedirs("data/processed", exist_ok=True)

filtered_sites.to_file(
    output_file,
    driver="GeoJSON"
)


print("----------------------------------")
print("SUCCESS")
print("----------------------------------")

print("Minimum allowed EV distance:", MIN_EV_DISTANCE, "meters")

print(
    "Original candidate sites:",
    len(sites)
)

print(
    "Candidates removed:",
    len(sites) - len(filtered_sites)
)

print(
    "Remaining candidate sites:",
    len(filtered_sites)
)

print(
    "New minimum EV distance:",
    round(filtered_sites["nearest_ev_distance"].min(), 2),
    "meters"
)

print("Saved to:", output_file)