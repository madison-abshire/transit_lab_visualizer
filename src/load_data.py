import pandas as pd
from maplib import Model

# If you don't want to use a graph database, the data can be accessed using
# this function and the N-triple file included
def load_data(path: str) -> Model:
    m = Model()
    m.read(file_path= path, format="ntriples", transient=True)
    return m