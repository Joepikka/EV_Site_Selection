# Thrissur EV Charging Site Selection

A GIS decision-support prototype for choosing electric-vehicle charging sites in Thrissur district, Kerala.
It builds a 1 km × 1 km candidate grid over the district, measures each cell's distance to roads and existing chargers, scores cells with multi-criteria decision analysis (MCDA), and shows the results on an interactive Streamlit map.

> Student portfolio project. The GIS layers use real public data; the model-training step uses a synthetic dataset (see Limits).

## Pipeline

| Step | Script | What it does |
| --- | --- | --- |
| 1 | `extract_thrissur.py` | Extracts the Thrissur boundary from geoBoundaries India district (ADM2) data |
| 2 | `create_grid.py` | Builds a 1 km × 1 km grid in a projected CRS |
| 3 | `download_roads.py` | Downloads the road network with OSMnx (OpenStreetMap) |
| 4 | `download_ev_stations.py` | Fetches existing chargers from the Open Charge Map API |
| 5 | `calculate_road_distance.py`, `calculate_ev_distance.py` | Distance from each cell to the nearest road and charger |
| 6 | `filter_ev_candidates.py` | Keeps feasible candidate cells |
| 7 | `mcda.py` | Min-max normalises benefit and cost criteria and computes a weighted suitability score and class |
| 8 | `train_model.py` | Trains a Random Forest classifier on the scored dataset |
| 9 | `app.py` | Streamlit + Folium map with layer controls and dataset statistics |

MCDA criteria: population density, distance from existing chargers and commercial activity (higher is better); road distance, slope and flood hazard (lower is better).

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Re-downloading the road network also needs `pip install osmnx`.

## Limits

- `generate_dataset.py` creates the 2,000-site training dataset from random values, and the Random Forest learns the MCDA labels computed from those same features. Its accuracy shows that it reproduces the scoring rule, not real-world site quality.
- Population density, slope, flood hazard and commercial scores are not yet joined from real GIS sources for every grid cell.
- MCDA weights are fixed by hand and have not been validated with planners or charger usage data.

## Tech

Python · GeoPandas · OSMnx · pandas · NumPy · scikit-learn · Streamlit · Folium
