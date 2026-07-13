import os
import geopandas as gpd
import osmnx as ox

# Input: real Thrissur district boundary
boundary_file = "data/processed/thrissur_boundary.geojson"

# Output: real Thrissur road network
output_file = "data/raw/roads/thrissur_roads.geojson"

print("Reading Thrissur boundary...")

thrissur = gpd.read_file(boundary_file)

# Combine geometry in case the file contains multiple features
thrissur_polygon = thrissur.geometry.union_all()

print("Downloading road network from OpenStreetMap...")
print("This may take several minutes. Please wait.")

# Download roads usable by vehicles inside the Thrissur district boundary
graph = ox.graph.graph_from_polygon(
    thrissur_polygon,
    network_type="drive",
    simplify=True
)

print("Converting road network to GeoDataFrame...")

nodes, roads = ox.graph_to_gdfs(graph)

# Keep useful road attributes
columns_to_keep = [
    column
    for column in ["osmid", "highway", "name", "length", "geometry"]
    if column in roads.columns
]

roads = roads[columns_to_keep].copy()

# Create output folder if necessary
os.makedirs("data/raw/roads", exist_ok=True)

# Save as GeoJSON
roads.to_file(output_file, driver="GeoJSON")

print("SUCCESS: Thrissur roads downloaded.")
print("Number of road segments:", len(roads))
print("Saved to:", output_file)
print("CRS:", roads.crs)