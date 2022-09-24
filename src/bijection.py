
import networkx as nx
import gudhi as gd
import numpy as np
import matplotlib.pyplot as plt
#from simplicial import *
import streamlit as st
import plotly.graph_objects as go


def get_skel(K,p):
    
    """
    Args: 
        K : gudhi.SimplexTree(), a simplicial complex
        p : int, a dimension
    Returns: 
        skel_new : list, a list of all p-simplices of K
    """
    
    skel = list(K.get_skeleton(p))
    skel_new = []
    for simplex in skel:
        if len(simplex[0]) == p+1:
            skel_new.append(simplex)
    return skel_new


    
def EP_to_LZZ(filtration, dgms):
    
    """This function translates the extended persistence barcode output of a 
    filtration on the simplicial complex X to its levelset zigzag barcode. 
    
    Args : 
        filtration : basic filtration on X
        dgms : output diagrams as returned by extended_persistence()
    Returns : 
        barcode_LZZ : corresponding levelset zigzag barcode
    """
    
    barcode_LZZ = []
    
    types = ["ORD","REL","EP+","EP-"]
    
    ORD = dgms[0]
    REL = dgms[1]
    EP = dgms[2]
    EP_ = dgms[3]
    
    for (dim,I) in ORD:
        
        J = [I[0],I[1]]
        
        barcode_LZZ.append(("ORD",dim,J))
        
    for (dim,I) in REL:
        
        J = [I[1],I[0]]
        
        barcode_LZZ.append(("REL",dim,J))
        
    for (dim,I) in EP:
        
        J = [I[0],I[1]]
        
        barcode_LZZ.append(("EP+",dim,J))
        
    for (dim,I) in EP_:
        
        J = [I[0],I[1]]
        
        barcode_LZZ.append(("EP-",dim,J))


    return barcode_LZZ

  
    
    

    
    

    
    

    





