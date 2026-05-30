import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objs as go

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
            colorscale="burg",
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
        width=1000,
        height=750,
    )

    st.plotly_chart(fig)