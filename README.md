# King County Metro Transit Lab Visualizer

An interactive Streamlit dashboard for exploring King County Metro transit data as a knowledge graph. Visualize stop density and transfer patterns across the network using SPARQL queries backed by either a live graph database or a locally loaded N-Triples file.

## Features

- **Stop Heatmap** — Visualize the geographic density of transit stops across King County
- **Transfer Density** — Map high-traffic transfer points and interchange patterns across the network
-  RDF/SPARQL — data is modeled as a knowledge graph and queried via SPARQL

## Data Backend

### Graph Database

Connect to a running SPARQL-compatible graph database (e.g. GraphDB or Fuseki). The `src/queries.py` module issues SPARQL queries via `SPARQLWrapper` against your configured endpoint.
The database client expects to connect on `http://localhost:7200` (so change if needed)

### Data
The RDF dataset used in this project is available as a .zip in the project structure. This can be used to populate your graph database.
The project for developing this resource is available here: https://github.com/lkbrennan97/IMT-542-Transit-Lab

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management and requires **Python ≥ 3.14**.

```bash
git clone https://github.com/madison-abshire/transit_lab_visualizer.git
cd transit_lab_visualizer
poetry install
```

## Running the App

```bash
poetry run streamlit run main.py
```

The app will open at `http://localhost:8501` by default.

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI and dashboard framework |
| `sparqlwrapper` | SPARQL queries against a remote graph database |
| `pandas` | Data manipulation |
| `plotly` | Interactive map visualizations |
| `numpy` | Numerical operations |


## Author

Madison Abshire — University of Washington ([mha6@uw.edu](mailto:mha6@uw.edu))