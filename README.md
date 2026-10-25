# Thrissur EV Site Selection

A Streamlit/GIS research prototype for exploring candidate EV charging locations in Thrissur district. The repository contains geographic preparation scripts, an interactive map, MCDA scoring, and a separate synthetic Random Forest demonstration.

## Two data workflows

| Workflow | Inputs and outputs | Interpretation |
| --- | --- | --- |
| Geographic exploration | GeoJSON under `data/raw/` and `data/processed/`; boundary, grid, stations, roads and candidate-distance layers | Inspect candidate geography and distance calculations. Missing layers are not evidence that a site is suitable. |
| Synthetic scoring and training | `generate_dataset.py` creates 2,000 random rows in `data/ev_sites.csv`; `mcda.py` writes `data/ev_sites_scored.csv`; `train_model.py` writes `models/ev_random_forest.pkl` | Demonstrates learning MCDA-derived labels. It does not validate demand, profitability or real-world charging-site suitability. |

The random latitude/longitude ranges in the generator are broader than a Thrissur boundary filter. Do not present the synthetic rows as surveyed Thrissur sites or assume the geographic pipeline supplies every model feature.

## Run the map

Use a Python virtual environment from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The map reads prepared files including `data/processed/thrissur_boundary.geojson`, `thrissur_grid.geojson`, `candidate_sites.geojson`, `candidate_sites_ev_distance.geojson`, `candidate_sites_filtered.geojson` and `candidate_sites_road_distance.geojson`. It also references station and road layers under `data/raw/`. Some views depend on these files being present.

Geographic scripts include [boundary extraction](extract_thrissur.py), [grid construction](create_grid.py), [station collection](download_ev_stations.py), [road collection](download_roads.py), [charger distance](calculate_ev_distance.py), [candidate filtering](filter_ev_candidates.py) and [road distance](calculate_road_distance.py). Inspect each script's configured inputs before running it; this documentation pass did not rerun collection.

## Reproduce the synthetic demonstration

Run in a disposable checkout or preserve existing outputs first: these scripts replace the generated CSV/model files.

```powershell
python generate_dataset.py
python mcda.py
python train_model.py
```

The generator uses NumPy seed 42. MCDA uses weighted min-max-normalized road distance, population density, existing-charger distance, slope, flood hazard and commercial score. Labels are low below 45, medium from 45 to below 70, and high from 70. The Random Forest uses 200 estimators, maximum depth 15, balanced class weights, and a stratified random 80/20 split with seed 42.

Accuracy against these labels measures reproduction of the scoring policy. Spatially independent evaluation, audited source provenance, sensitivity analysis and independent site outcomes are still needed before planning decisions.

## Verification scope

This README was checked against the repository's scripts and paths on 25 October 2026. No dependencies were installed, data regenerated, model trained, accuracy measured or application started during this documentation change. Dependencies are listed in [requirements.txt](requirements.txt); no reproducible environment lock or passing test result is asserted.
