import networkx as nx
import plotly.graph_objects as go
import streamlit as st
from pyvis.network import Network
import numpy as np


def cycle() -> tuple:

    """
    Returns a 3-tuple of data about the 6-cycle graph, containing :
        - the space itself as a string whose value is a list of edges
        - a filtration on the space as a string
        - a nx.Graph() object
    """
    edges = [[i, i + 1] for i in range(5)] + [[5, 0]]
    G = nx.Graph()
    G.add_nodes_from(range(5))
    filtration = str([([0], 15), ([1], 16), ([5], 16), ([2], 17), ([4], 17), ([3], 18)])
    G.add_edges_from(edges)
    space = str(edges)

    return (space, filtration, G)


def complete() -> tuple:

    """
    Returns a 3-tuple of data about the complete graph on 8 nodes, containing :
        - the space itself as a string whose value is a list of edges
        - a filtration on the space as a string
        - a nx.Graph() object
    """

    G = nx.complete_graph(8)
    filtration = str([([n], n) for n in G.nodes()])

    space = str([list(edge) for edge in list(G.edges())])

    return (space, filtration, G)


def make_point(fig: go.Figure(),
               a: float,
               b: float,
               color: str,
               row: int,
               col: int,
               dim: int,
               interval: tuple | list) -> None:
    """
    Used to plot a single point in a levelset or extended persistence diagram.
    """

    fig.add_trace(go.Scatter(
        x=[a, b], y=[a, b],
        fill=None,
        mode='lines',
        line_color='lightblue',
        showlegend=False
    ), row=row, col=col)

    fig.add_trace(go.Scatter(
        x=[interval[0]], y=[interval[1]],
        fill=None,
        mode='markers',
        name='dim ' + str(dim),
        marker=dict(
            color=color,
            size=6,
            line=dict(
                color=color,
                width=0.5
            )
        ),
        showlegend=False
    ), row=row, col=col)


def plot_diagram_plotly(fig: go.Figure(), dgms: list, filt: list, class_: str) -> None:
    """
    Plots the extended / levelset persistence diagram with Plotly.

    Args:
        class_ : is either 'extended' or 'levelset'.
    """
    def get_col(i: int, class_: str) -> int:
        if class_ == 'extended':
            return 1 + i % 2
        elif class_ == 'levelset':
            return 3 + i % 2
        else:
            raise ValueError("Class attribute must be either 'extended' or 'levelset'.")

    a = min(filt)
    b = max(filt)
    colors = ['LightSkyBlue', 'aquamarine', 'cornflowerblue', 'violet']

    for i, color in enumerate(colors):
        for (dim, I) in dgms[i]:
            make_point(fig=fig,
                       a=a,
                       b=b,
                       color=color,
                       row=1 + np.floor(i / 2),
                       col=get_col(i, class_),
                       dim=dim,
                       interval=I)


def to_barcode_ext(dgms: list) -> list[dict]:
    """
    Receives extended dgms and outputs an extended barcode.
    """
    barcode = []
    types = ["ORD", "REL", "EP+", "EP-"]

    for i, t in enumerate(types):
        for point in dgms[i]:
            interval = [point[1][0], point[1][1]]
            barcode.append({
                "dimension": point[0],
                "interval": interval,
                "type": t
            })

    return barcode


def threshold(G: nx.Graph(), t: float):
    """
    Returns the pyvis network obtained from removing edges in the graph G whose weight is greater than t.

    NB. This function is used to observe a filtrated graph G as it evolves with its filtration.
    """

    H = G.copy()
    for e in G.edges.data():
        if e[2]['weight'] > t:
            H.remove_edge(*e[:2])
    nt = Network("340px", "860px", notebook=True)
    nt.from_nx(H)

    return nt


def graph_time_series(space, filtration) -> list[tuple]:

    "Returns a list of embedded yvis networks obtained from a filtration on a space."

    st.markdown("Use the slider below to observe how the complex evolves with its filtration.")

    f = eval(filtration)
    f_vertices = [v[0] for v in f]
    f_values = [v[1] for v in f]
    G = nx.Graph()

    for edge in eval(space):
        i1 = f_vertices.index([edge[0]])
        i2 = f_vertices.index([edge[1]])
        w1 = f_values[i1]
        w2 = f_values[i2]
        w = max(w1, w2)
        G.add_edge(*edge, weight=w)

    time_series = [(threshold(G, t), t) for t in f_values]

    return time_series
