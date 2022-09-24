import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import streamlit as st
from pyvis.network import Network



def cycle():

    """Returns a 3-tuple of data about the 6-cycle graph, containing :
        - the space itself as a string whose value is a list of edges
        - a filtration on the space as a string 
        - a nx.Graph() object"""
    
    G = nx.Graph()
    G.add_nodes_from(range(5))
    filtration = str([([0],15),([1],16),([5],16),([2],17),([4],17),([3],18)])
    G.add_edges_from([[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]])
    space = str([[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]])
    
    return (space, filtration, G)


def complete():

    """
    Returns a 3-tuple of data about the complete graph on 8 nodes, containing :
        - the space itself as a string whose value is a list of edges
        - a filtration on the space as a string 
        - a nx.Graph() object
    """
    
    G = nx.complete_graph(8)
    filtration = str([([n],n) for n in G.nodes()])
    
    space = str([list(edge) for edge in list(G.edges())])
    
    return (space, filtration, G)


def make_point(fig, a, b, color, row, col, dim, I):

    "Used to plot a single point in a levelset or extended persistence diagram."

    fig.add_trace(go.Scatter(x=[a,b], y=[a,b],
            fill=None,
            mode='lines',
            line_color='lightblue',
            showlegend=False
            ), row=row, col=col)
    
    fig.add_trace(go.Scatter(x=[I[0]], y=[I[1]],
            fill=None,
            mode='markers',
            name = 'dim ' + str(dim),
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


def plot_extended_diagram_plotly(fig, dgms, filt):

    "Plots the extended persistence diagram with Plotly."
    
    a = min(filt)
    b = max(filt)
    
    for (dim,I) in dgms[0]:
        
        make_point(fig, a, b, 'LightSkyBlue', 1, 1, dim, I)
        
    for (dim,I) in dgms[1]:

        make_point(fig, a, b, 'aquamarine', 1, 2, dim, I)
        
    for (dim,I) in dgms[2]:
        
        make_point(fig, a, b, 'cornflowerblue', 2, 1, dim, I)
        
    for (dim,I) in dgms[3]:
        
        make_point(fig, a, b, 'violet', 2, 2, dim, I)
        
        
        
def plot_levelset_diagram_plotly(fig, dgms, filt):

    "Plots the levelset zigzag diagram with Plotly."
    
    a = min(filt)
    b = max(filt)
    
    for (dim,I) in dgms[0]:
        
        make_point(fig, a, b, 'LightSkyBlue', 1, 3, dim, I)
        
    for (dim,I) in dgms[1]:

        make_point(fig, a, b, 'aquamarine', 1, 4, dim, I)
        
    for (dim,I) in dgms[2]:
        
        make_point(fig, a, b, 'cornflowerblue', 2, 3, dim, I)
        
    for (dim,I) in dgms[3]:
        
        make_point(fig, a, b, 'violet', 2, 4, dim, I)
    

def to_barcode_ext(dgms):
    
    """Receives extended dgms and outputs an extended barcode."""
    
    ORD = dgms[0]
    REL = dgms[1]
    EP = dgms[2]
    EP_ = dgms[3]
    
    barcode = [] # to be a list of dict
    
    for point in ORD:
        
        interval = [point[1][0], point[1][1]]
        barcode.append({
            "dimension":point[0],
            "interval":interval,
            "type":'ORD'
            })
        
    for point in REL:
        
        interval = [point[1][0], point[1][1]]
        barcode.append({
            "dimension":point[0],
            "interval":interval,
            "type":'REL'
            })   
        
    for point in EP:
        
        interval = [point[1][0], point[1][1]]
        barcode.append({
            "dimension":point[0],
            "interval":interval,
            "type":'EP+'
            })  
    for point in EP_:
        
        interval = [point[1][0], point[1][1]]
        barcode.append({
            "dimension":point[0],
            "interval":interval,
            "type":'EP-'
            })   
        
        
    return barcode
        



def threshold(G,t):

    """
    Args :
         G : nx.Graph()
         t : float value
    Returns the pyvis network obtained from removing edges in G whose weight is greater than t.
    
    NB. This function is used to observe a filtrated graph G as it evolves with its filtration.
    """
    
    H = G.copy()
    
    for e in G.edges.data():
        
        if e[2]['weight'] > t:
        
            H.remove_edge(*e[:2])
            
    nt = Network("340px", "860px",notebook=True)
    nt.from_nx(H)
    
    return nt
        
        
        
def graph_time_series(space, filtration):

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
        w = max(w1,w2)
            
        G.add_edge(*edge, weight=w)
        
    time_series = [(threshold(G,t),t) for t in f_values]

    return time_series



        
    
    
    
    