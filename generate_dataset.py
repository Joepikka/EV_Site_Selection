import os
import numpy as np
import pandas as pd

np.random.seed(42)

NUMBER_OF_SITES = 2000

os.makedirs("data", exist_ok=True)

data = pd.DataFrame({
    "latitude": np.random.uniform(8.2, 12.8, NUMBER_OF_SITES),

    "longitude": np.random.uniform(74.8, 77.5, NUMBER_OF_SITES),

    "road_distance": np.random.uniform(0, 10, NUMBER_OF_SITES),

    "population_density": np.random.uniform(100, 10000, NUMBER_OF_SITES),

    "existing_charger_distance": np.random.uniform(0, 25, NUMBER_OF_SITES),

    "slope": np.random.uniform(0, 45, NUMBER_OF_SITES),

    "flood_hazard": np.random.uniform(0, 1, NUMBER_OF_SITES),

    "commercial_score": np.random.uniform(0, 1, NUMBER_OF_SITES)
})

data.to_csv("data/ev_sites.csv", index=False)

print("Dataset created successfully!")

print(data.head())