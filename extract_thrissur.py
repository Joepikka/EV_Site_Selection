import geopandas as gpd
import os

# Input India district boundary file
input_file = "data/raw/boundary/geoBoundaries-IND-ADM2.geojson"

# Output Thrissur boundary file
output_file = "data/processed/thrissur_boundary.geojson"

# Read India district boundaries
districts = gpd.read_file(input_file)

# Show available columns
print("Columns:", districts.columns.tolist())

# Find Thrissur district
thrissur = districts[
    districts["shapeName"].str.contains("Thrissur", case=False, na=False)
]

# Check whether Thrissur was found
if thrissur.empty:
    print("ERROR: Thrissur district was not found.")
    print("Available district names:")
    print(districts["shapeName"].tolist())
else:
    # Create output folder if necessary
    os.makedirs("data/processed", exist_ok=True)

    # Save Thrissur boundary
    thrissur.to_file(output_file, driver="GeoJSON")

    print("SUCCESS: Thrissur boundary extracted.")
    print("Saved to:", output_file)
    print("CRS:", thrissur.crs)