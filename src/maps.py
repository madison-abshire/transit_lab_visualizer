import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objs as go
from src.calculations import haversine

def heatmap(df: pd.DataFrame) -> None:
    fig = px.density_map(
        df,
        lat='latBucket',
        lon='lonBucket',
        z='stopCount',
        color_continuous_scale="thermal",
        radius=10,
        width=750,
        height=500,
        map_style="carto-positron",
    )
    st.plotly_chart(fig)

def transfer_points(df: pd.DataFrame) -> None:
    df["routeCount"] = pd.to_numeric(df["routeCount"], errors="coerce")
    fig = go.Figure(go.Scattermap(
        lat=df["lat"],
        lon=df["lon"],
        mode="markers",
        marker=go.scattermap.Marker(
            size=df["routeCount"] / df["routeCount"].max() * 30,  # normalize size
            color=df["routeCount"].astype("float64"),
            colorscale="dense",
            showscale=True,
            colorbar=dict(title="Route Count"),
            cmin=df["routeCount"].min(),
            cmax=df["routeCount"].max(),
        ),
        text=df["stop_name"],
        hovertemplate="<b>%{text}</b><br>Routes: %{marker.color}<extra></extra>"
    ))

    fig.update_layout(
        map=dict(
            style="carto-positron",
            center=dict(
                lat=df["lat"].median(),
                lon=df["lon"].median()
            ),
            zoom=10
        ),
        title="Transfer Points",
        width=750,
        height=500,
    )

    st.plotly_chart(fig)

def gap_analysis(df: pd.DataFrame) -> None:
    df["distance_m"] = haversine(
        df["lat1"], df["lon1"],
        df["lat2"], df["lon2"]
    )

    mean_dist = df["distance_m"].mean()
    std_dist = df["distance_m"].std()
    threshold = mean_dist + (2 * std_dist)

    gaps = df[df["distance_m"] > threshold].sort_values("distance_m", ascending=False)

    gaps["mid_lat"] = (gaps["lat1"] + gaps["lat2"]) / 2
    gaps["mid_lon"] = (gaps["lon1"] + gaps["lon2"]) / 2

    fig = go.Figure(go.Scattermap(
        lat=gaps["mid_lat"],
        lon=gaps["mid_lon"],
        mode="markers",
        marker=go.scattermap.Marker(
            size=gaps["distance_m"] / gaps["distance_m"].max() * 10,
            color=gaps["distance_m"].astype("float64"),
            colorscale="Burg",
            showscale=True,
            colorbar=dict(title="Distance (m)"),
            cmin=gaps["distance_m"].min(),
            cmax=gaps["distance_m"].max(),
        ),
        text=gaps["name1"] + " → " + gaps["name2"],
        hovertemplate="<b>%{text}</b><br>Distance: %{marker.color:.0f}m<extra></extra>"
    ))

    fig.update_layout(
        map=dict(
            style="carto-positron",
            center=dict(
                lat=gaps["mid_lat"].mean(),
                lon=gaps["mid_lon"].mean()
            ),
            zoom=11
        ),
        width=750,
        height=500,
        title="Stop Gap Analysis — Segments Beyond 2 Standard Deviations (Seattle Proper)"
    )

    st.plotly_chart(fig)