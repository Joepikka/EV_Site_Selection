import os
import numpy as np
import geopandas as gpd
from shapely.geometry import box

# Input Thrissur boundary
boundary_file = "data/processed/thrissur_boundary.geojson"

# Output files
grid_file = "data/processed/thrissur_grid.geojson"
candidate_file = "data/processed/candidate_sites.geojson"

# Actual grid size in meters
GRID_SIZE = 1000

print("Reading Thrissur boundary...")

boundary = gpd.read_file(boundary_file)

# Convert WGS84 coordinates to UTM Zone 43N.
# A projected CRS is required to create true 1000 m x 1000 m cells.
boundary_projected = boundary.to_crs(epsg=32643)

print("Creating 1 km x 1 km grid...")

minx, miny, maxx, maxy = boundary_projected.total_bounds

x_coordinates = np.arange(minx, maxx, GRID_SIZE)
y_coordinates = np.arange(miny, maxy, GRID_SIZE)

grid_cells = []

for x in x_coordinates:
    for y in y_coordinates:
        cell = box(
            x,
            y,
            x + GRID_SIZE,
            y + GRID_SIZE
        )

        grid_cells.append(cell)

grid = gpd.GeoDataFrame(
    geometry=grid_cells,
    crs=boundary_projected.crs
)

print("Removing cells outside Thrissur...")

# Keep cells that intersect Thrissur
grid = grid[grid.intersects(boundary_projected.geometry.union_all())].copy()

# Clip boundary cells so grid does not extend outside Thrissur
grid = gpd.clip(grid, boundary_projected)

# Remove empty geometries
grid = grid[~grid.geometry.is_empty].copy()

# Add unique site/grid ID
grid = grid.reset_index(drop=True)

grid["site_id"] = [
    f"THR_{number:04d}"
    for number in range(1, len(grid) + 1)
]

# Calculate actual area after clipping
grid["area_km2"] = grid.geometry.area / 1_000_000

print("Creating candidate points...")

# representative_point() guarantees that the point lies inside the cell,
# including irregular cells near the district boundary.
candidate_sites = grid[["site_id", "geometry"]].copy()

candidate_sites["geometry"] = candidate_sites.geometry.representative_point()

# Convert outputs to latitude/longitude for map display
grid_wgs84 = grid.to_crs(epsg=4326)

candidate_sites_wgs84 = candidate_sites.to_crs(epsg=4326)

candidate_sites_wgs84["longitude"] = candidate_sites_wgs84.geometry.x
candidate_sites_wgs84["latitude"] = candidate_sites_wgs84.geometry.y

# Create output directory
os.makedirs("data/processed", exist_ok=True)

# Save grid and candidate locations
grid_wgs84.to_file(grid_file, driver="GeoJSON")

candidate_sites_wgs84.to_file(candidate_file, driver="GeoJSON")

print("SUCCESS: Candidate grid created.")
print("Number of grid cells:", len(grid_wgs84))
print("Number of candidate sites:", len(candidate_sites_wgs84))
print("Saved grid to:", grid_file)
print("Saved candidate sites to:", candidate_file)