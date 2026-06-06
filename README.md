# King County Metro Knowledge Graph

**Madison Abshire & Lincoln Brennan, University of Washington, Spring 2026**

Transit analysts and planners working with King County Metro schedule data need to answer network-level questions: where service concentrates, which stops are key transfer points, and where gaps in transit coverage occur. This project transforms static GTFS (https://gtfs.org/) schedule files into a queryable RDF knowledge graph and interactive visualization dashboard, making those questions answerable with a single SPARQL query instead of multi-file joins.

**Core question:** How can GTFS transit schedule data be restructured to make network-level patterns directly queryable and visually explorable?

_**There is a seperate project containing data preparation workflows and process documents: https://github.com/lkbrennan97/IMT-542-Transit-Lab**_

---

## Features

- **Stop Heatmap**: Geographic density of transit stops across King County using Plotly density map
- **Transfer Density**: High-traffic transfer points sized and colored by route count
- **Gap Analysis**: Inter-stop distance heatmap identifying express segments and sparse coverage areas
- **SPARQL Backend**: All visualizations driven by SPARQL queries against a live graph database or local N-Triples file

---

## Data Backend

### Graph Database

Connect to a running SPARQL-compatible graph database (GraphDB or Fuseki). The `src/queries.py` module issues SPARQL queries via `SPARQLWrapper` against your configured endpoint.

Default endpoint: `http://localhost:7200` — update if needed.

Queries can be tested and explored directly in the GraphDB Workbench before running through the app.

---

## Scope

**In scope:**
- Routes, trips, stops, and stop times from King County Metro GTFS feeds
- RDF knowledge graph construction using the [GTFS ontology](https://gtfs.org/documentation/schedule/reference/#field-definitions)
- SPARQL-based network analysis: stop centrality, transfer points, gap analysis
- Interactive map visualizations via Plotly
- Portable N-Triples export for use in any SPARQL-compatible triplestore
- GraphDB and Fuseki compatibility

**Out of scope:**
- Real-time arrival data (GTFS-RT)
- Fare and ticketing data
- Accessibility attributes
- Multi-agency feeds beyond King County Metro

---

## Why a Knowledge Graph?

GTFS data is distributed as flat CSV/TXT files. These are well-structured for storage but require multiple joins to answer network questions. The FAIR assessment of the source files:

| Principle | Assessment |
|---|---|
| **Findable** | Yes: GTFS is a published open standard with consistent field names |
| **Accessible** | Partially: files are downloadable but require tooling to join and interpret |
| **Interoperable** | Limited: CSV/TXT has no semantic meaning; field relationships are implicit |
| **Reusable** | Limited: without a schema, analysts must reverse-engineer the relational structure |

Transforming GTFS to RDF makes the relationships between routes, trips, stops, and times explicit and directly traversable via SPARQL

---

## FAIR Assessment of the Knowledge Graph

The following assesses how the resulting knowledge graph compares to the source GTFS files across the four FAIR principles. Where the graph falls short, the reason and current workaround are noted.

**Findable**

The graph is not publicly hosted and has no persistent identifier (DOI or URI). It is findable only to those who have access to this repository and the included N-Triples zip file. The graph uses globally unique IRIs for every node and property (e.g. `http://imt542.org/transit/stop/987`), which would support discoverability if the graph were published to a public endpoint. Current status: partially findable within the project context, not findable on the open web.

**Accessible**

The N-Triples file is included in the repository zip and can be loaded into any SPARQL-compatible triplestore (GraphDB, Fuseki) or queried locally via `maplib`. No authentication is required to access the file from the repository. As of yet, there is no live SPARQL endpoint, so  users must load the file themselves. Current status: accessible via file transfer, not accessible via a queryable endpoint.

**Interoperable**

This is the strongest dimension of the knowledge graph relative to the source files. The graph uses GTFS terminology for all transit concepts and N-Triples serialization which is parseable by any RDF-compliant tool. Any system that speaks RDF and SPARQL can consume this graph without custom parsing logic. Current status: fully interoperable within the RDF/SPARQL ecosystem.

**Reusable**

The graph schema is documented in this README and mirrors the published GTFS ontology, so the meaning of every predicate is externally defined and stable. The N-Triples file is self-contained and includes all relationships needed to reconstruct the network without the original GTFS source files. The transformation workflow can be adapted to any transit system that uses the GTFS standard.

---

## Ontology & Metadata

The graph preserves the relationships and key metadata from the GTFS schema, reduced to the fields needed for network analysis:

```
Stop Time ──from──> Trip ──belongs_to──> Route
          ──at───> Stop
```

| Node Type | Field | Description |
|---|---|---|
| route | route_short_name | Route number, e.g. "3" |
| route | route_description | e.g. "Capitol Hill - Downtown Seattle" |
| stop | stop_name | e.g. "1st Ave & Spring St" |
| stop | stop_lat | Latitude |
| stop | stop_lon | Longitude |
| trip | route | Route node belonging to trip |
| trip | trip_headsign | Readable identifier, e.g. "Rainier Beach" |
| stop_time | trip | Trip node belonging to stop time |
| stop_time | stop | Stop node belonging to stop time |
| stop_time | stop_sequence | Relative position of stop in trip sequence |
| stop_time | arrival_time | When bus arrives |
| stop_time | departure_time | When bus departs |

---

## Transformation Pipeline

```
1. GTFS Files        2. Data Conversion     3. Construction
   Zipped .txt          Reformat CSV rows      Construct RDF
   files readable        into RDF OTTR          knowledge graph
   as CSVs              templates              in memory
                              ↓
                    4. Serialization       5. Deployment
                       Write graph to        Import N-Triples
                       N-Triples format      into graph database
                       for sharing           or load in memory
```

_**The transformation workflow that produces the N-Triples file as well as process documents are available at: https://github.com/lkbrennan97/IMT-542-Transit-Lab**_

---

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management and requires **Python ≥ 3.14**.

```bash
git clone https://github.com/madison-abshire/transit_lab_visualizer.git
cd transit_lab_visualizer
poetry install
```

## Running the App

```bash
streamlit run main.py
```

The app opens at `http://localhost:8501` by default.

---

## Test Plan

**Unit tests:** Test suite covering individual SPARQL query outputs and data transformation steps.

**End-to-end tests:** Full pipeline from Streamlit front end through SPARQLWrapper to GraphDB back end, verifying query results match expected node and edge counts.

**Validation checks:**
- `COUNT(DISTINCT ?route)` matches the number of routes loaded from the source GTFS feed
- All Stop nodes have `geo:lat` and `geo:long` values (no null coordinates)
- Stop sequence is contiguous per trip (no gaps in `stop_sequence`)

**Manual tests:**
(These are run aginst the companion project at https://github.com/lkbrennan97/IMT-542-Transit-Lab)
- GitHub installation instructions followed from a clean environment
- Jupyter notebook tested cell-by-cell and end-to-end
- Output N-Triples file validated against a SPARQL endpoint

---

## Known Limitations and Planned Fixes

**Gap analysis visuals:** The inter-stop distance visualization currently plots midpoints rather than line segments, making individual gaps hard to locate geographically. Fix: render as line segments between consecutive stop coordinates.

**Streamlit startup time:** Cold start with the full N-Triples file is slow. Fix: pre-serialize a filtered subgraph per route selection and cache SPARQL results.

---

## Performance

**Known bottlenecks:**
- Time to serialize the full graph
- Time to query across large graphs
- Size of query result sets for full-network queries

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI and dashboard framework |
| `sparqlwrapper` | SPARQL queries against a remote graph database |
| `pandas` | Data manipulation and GTFS filtering |
| `plotly` | Interactive map visualizations |
| `numpy` | Numerical operations (haversine distance) |

---

## Authors

Madison Abshire — University of Washington (mha6@uw.edu)  
Lincoln Brennan — University of Washington
