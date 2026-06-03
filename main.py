import streamlit as st
from src.queries import stop_density, transfer_density, stop_distances
from src.maps import heatmap, transfer_points, gap_analysis

def main() -> None:
    st.set_page_config(page_title = "King County Metro Transit Lab", layout="wide")
    st.title("King County Metro Transit Lab")

    t1, t2, t3 = st.tabs(["Stop Heatmap", "Transfer Density", "Gap Analysis"])
    with t1:
        st.subheader("Stop Heatmap")
        data = stop_density()
        heatmap(data)
    with t2:
        st.subheader("Transfer Density")
        data = transfer_density()
        transfer_points(data)
    with t3:
        st.subheader("Gap Analysis")
        data = stop_distances()
        gap_analysis(data)

if __name__ == '__main__':
    main()

