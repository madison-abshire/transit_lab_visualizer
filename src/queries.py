import pandas as pd
from maplib import Model
from src.graphdb_client import GraphDBClient

GTFS_STR = "http://vocab.gtfs.org/terms#"
GEO_STR = "http://www.w3.org/2003/01/geo/wgs84_pos#"
gdb = GraphDBClient()

def stop_density() -> pd.DataFrame:
    data = gdb.query(f"""
            PREFIX gtfs: <{GTFS_STR}>
            PREFIX geo:  <{GEO_STR}>
            SELECT ?latBucket ?lonBucket (COUNT(DISTINCT ?stop) AS ?stopCount)
            WHERE {{
                {{
                    SELECT ?stop
                           (ROUND(?stop_lat * 500) / 500 AS ?latBucket)
                           (ROUND(?stop_lon * 500) / 500 AS ?lonBucket)
                    WHERE {{
                        ?stop a gtfs:Stop ;
                              geo:lat  ?stop_lat ;
                              geo:long ?stop_lon .
                    }}
                }}
            }}
            GROUP BY ?latBucket ?lonBucket
            ORDER BY DESC(?stopCount)
        """)
    df = pd.DataFrame(data, columns=["latBucket", "lonBucket", "stopCount"])
    df["latBucket"] = df["latBucket"].astype(float)
    df["lonBucket"] = df["lonBucket"].astype(float)
    df["stopCount"] = df["stopCount"].astype(int)
    return df

def transfer_density() -> pd.DataFrame:
    data = gdb.query(f"""
        PREFIX gtfs: <{GTFS_STR}>
        PREFIX geo:  <{GEO_STR}>
        SELECT ?stop_name ?lat ?lon
        (COUNT(DISTINCT ?route) AS ?routeCount)
        WHERE {{
            ?st    gtfs:stop ?stop ;
                   gtfs:trip ?trip .
            ?trip  gtfs:route ?route .
            ?stop  gtfs:name  ?stop_name ;
                   geo:lat    ?lat ;
                   geo:long   ?lon .
        }}
        GROUP BY ?stop_name ?lat ?lon
        HAVING (COUNT(DISTINCT ?route) > 1)
        ORDER BY DESC(?routeCount)
    """)
    df = pd.DataFrame(data, columns=["stop_name", "lat", "lon", "routeCount"])
    df["routeCount"] = df["routeCount"].astype(int)
    df["lat"] = df["lat"].astype(float)
    df["lon"] = df["lon"].astype(float)

    return df

def stop_distances() -> pd.DataFrame:
    routes = [31, 32, 40, 43, 44, 45, 48, 49] #[1, 2, 8, 10, 11, 12, 13, 31, 32, 40, 43, 44, 45, 48, 49, 60, 62, 65, 67, 75]
    route_filter = ", ".join([f'"{r}"' for r in routes])

    data = gdb.query(f"""
        PREFIX gtfs: <{GTFS_STR}>
        PREFIX geo:  <{GEO_STR}>
        SELECT ?route_name ?trip ?seq1 ?seq2
           ?name1 ?lat1 ?lon1
           ?name2 ?lat2 ?lon2
        WHERE {{
            ?route gtfs:route_short_name ?route_name ;
                 gtfs:trip ?trip .
            ?st1 gtfs:trip ?trip ;
                 gtfs:stop_sequence ?seq1 ;
                 gtfs:stop ?stop1 .
            ?st2 gtfs:trip ?trip ;
                 gtfs:stop_sequence ?seq2 ;
                 gtfs:stop ?stop2 .
            ?stop1 gtfs:name ?name1 ; geo:lat ?lat1 ; geo:long ?lon1 .
            ?stop2 gtfs:name ?name2 ; geo:lat ?lat2 ; geo:long ?lon2 .
            FILTER(xsd:integer(?seq2) = xsd:integer(?seq1) + 1 && ?route_name IN ({route_filter}))
        }}
    """)
    df = pd.DataFrame(data, columns=["route_name", "trip", "seq1", "seq2", "name1", "lat1", "lon1", "name2", "lat2", "lon2"])

    df["lat1"] = df["lat1"].astype(float)
    df["lon1"] = df["lon1"].astype(float)
    df["lat2"] = df["lat2"].astype(float)
    df["lon2"] = df["lon2"].astype(float)

    return df

