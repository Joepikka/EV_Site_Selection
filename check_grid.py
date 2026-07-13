import geopandas as gpd
import folium

boundary = gpd.read_file("data/processed/thrissur_boundary.geojson")
grid = gpd.read_file("data/processed/thrissur_grid.geojson")
sites = gpd.read_file("data/processed/candidate_sites.geojson")

print("Boundary features:", len(boundary))
print("Grid cells:", len(grid))
print("Candidate sites:", len(sites))

# Create map centered on Thrissur
center = boundary.geometry.union_all().centroid

m = folium.Map(
    location=[center.y, center.x],
    zoom_start=9
)

# Add district boundary
folium.GeoJson(
    boundary,
    name="Thrissur Boundary",
    style_function=lambda feature: {
        "color": "black",
        "weight": 3,
        "fillOpacity": 0
    }
).add_to(m)

# Add 1 km grid
folium.GeoJson(
    grid,
    name="1 km Candidate Grid",
    style_function=lambda feature: {
        "color": "blue",
        "weight": 0.5,
        "fillOpacity": 0.05
    }
).add_to(m)

# Add candidate points
for _, site in sites.iterrows():
    folium.CircleMarker(
        location=[site.geometry.y, site.geometry.x],
        radius=1,
        weight=1,
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

folium.LayerControl().add_to(m)

output_file = "data/processed/check_grid_map.html"

m.save(output_file)

print("SUCCESS: Grid validation map created.")
print("Saved to:", output_file)