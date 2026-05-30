import pandas as pd
from maplib import Model
from src.graphdb_client import GraphDBClient

GTFS_STR = "http://vocab.gtfs.org/terms#"
gdb = GraphDBClient()

def stop_density() -> pd.DataFrame:
    data = gdb.query(f"""
            PREFIX gtfs: <{GTFS_STR}>
            PREFIX geo:  <http://www.w3.org/2003/01/geo/wgs84_pos#>
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
        PREFIX geo:  <http://www.w3.org/2003/01/geo/wgs84_pos#>
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
