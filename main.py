import streamlit as st
# Use load_data module if not using a graph database
# from src.load_data import load_data
from src.queries import stop_density, transfer_density
from src.maps import heatmap, transfer_points

def main() -> None:
    st.set_page_config(page_title = "King County Metro Transit Lab", layout="wide")
    st.title("King County Metro Transit Lab")

    # m = load_data(path = "data/transit_ntriples.nt")

    t1, t2 = st.tabs(["Stop Heatmap", "Transfer Density"])
    with t1:
        st.subheader("Stop Heatmap")
        data = stop_density()
        heatmap(data)
    with t2:
        st.subheader("Transfer Density")
        data = transfer_density()
        transfer_points(data)

if __name__ == '__main__':
    main()

