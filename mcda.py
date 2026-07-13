import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# Read the candidate EV site dataset
data = pd.read_csv("data/ev_sites.csv")


# Create the scaler
scaler = MinMaxScaler()


# -----------------------------------
# BENEFIT FEATURES
# Higher value = better
# -----------------------------------

benefit_features = [
    "population_density",
    "existing_charger_distance",
    "commercial_score"
]


# -----------------------------------
# COST FEATURES
# Lower value = better
# -----------------------------------

cost_features = [
    "road_distance",
    "slope",
    "flood_hazard"
]


# Normalize benefit features

for feature in benefit_features:

    data[feature + "_norm"] = scaler.fit_transform(
        data[[feature]]
    )


# Normalize cost features

for feature in cost_features:

    normalized_value = scaler.fit_transform(
        data[[feature]]
    )

    # Reverse the normalized value
    # because lower values are better

    data[feature + "_norm"] = 1 - normalized_value


# -----------------------------------
# MCDA WEIGHTS
# -----------------------------------

weights = {
    "road_distance_norm": 0.25,
    "population_density_norm": 0.20,
    "existing_charger_distance_norm": 0.15,
    "slope_norm": 0.10,
    "flood_hazard_norm": 0.15,
    "commercial_score_norm": 0.15
}


# Create empty suitability score

data["suitability_score"] = 0.0


# Calculate weighted suitability score

for feature, weight in weights.items():

    data["suitability_score"] += (
        data[feature] * weight
    )


# Convert score from 0-1 to 0-100

data["suitability_score"] = (
    data["suitability_score"] * 100
)


# -----------------------------------
# CREATE SUITABILITY CLASSES
# -----------------------------------

def create_label(score):

    if score >= 70:
        return 2

    elif score >= 45:
        return 1

    else:
        return 0


data["suitability_class"] = (
    data["suitability_score"].apply(create_label)
)


# Save the result

data.to_csv(
    "data/ev_sites_scored.csv",
    index=False
)


print("MCDA scoring completed successfully!")


print(
    data[
        [
            "latitude",
            "longitude",
            "suitability_score",
            "suitability_class"
        ]
    ].head()
)


print("\nClass Distribution:")

print(
    data["suitability_class"].value_counts()
)