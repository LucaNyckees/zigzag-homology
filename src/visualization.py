import networkx as nx
import gudhi as gd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from helpers import to_barcode_ext

def make_interval(fig, bar, i, name, color1, color2, color3, row, col):
    
    fig.add_trace(go.Scatter(x=[bar[2][0],bar[2][1]], y=[i,i],
        fill=None,
        mode='lines',
        name = name,
        line_color=color1
        ), row=row, col=col)
    fig.add_trace(go.Scatter(x=[bar[2][1]], y=[i],
        fill=None,
        mode='markers',
        name = name,
        marker=dict(
            color=color2,
            size=8,
            line=dict(
                color=color1,
                width=0.5
            )
        ),
        showlegend=False
        ), row=row, col=col)
    fig.add_trace(go.Scatter(x=[bar[2][0]], y=[i],
        fill=None,
        mode='markers',
        name = name,
        marker=dict(
            color=color3,
            size=8,
            line=dict(
                color=color1,
                width=0.5
            )
        ),
        showlegend=False
        ), row=row, col=col)



def plot_barcode_LZZ_plotly(fig, barcode_LZZ):
    
    i = 1

    for bar in barcode_LZZ:

        if bar[0]=='ORD':
            
            make_interval(fig, bar, i, 'Type I', 'LightSkyBlue', 'white', 'LightSkyBlue', 1, 2)
            
        elif bar[0]=='REL':
            
            make_interval(fig, bar, i, 'Type II', 'aquamarine', 'aquamarine', 'white', 1, 2)
            
        elif bar[0]=='EP+':
            
            make_interval(fig, bar, i, 'Type III', 'cornflowerblue', 'cornflowerblue', 'cornflowerblue', 1, 2)
               
        elif bar[0]=='EP-':
            
            make_interval(fig, bar, i, 'Type IV', 'violet', 'white', 'white', 1, 2)
            
            
        i+=1
        
    fig['layout'].update({
        'showlegend': True
    })
    
    fig.update_yaxes(range=(0,len(barcode_LZZ)+1))
    
    
    
    
    
def plot_extended_barcode_plotly(fig, dgms, filt):
    
    m = len(dgms[0])+len(dgms[1])+len(dgms[2])+len(dgms[3])
    
    
    barcode = to_barcode_ext(dgms)
    
    filt_max = max(filt)
    l = filt_max-min(filt)
    
    plot_barcode_plotly(fig, barcode, l)
    
    fig.add_trace(go.Scatter(x=[filt_max,filt_max], y=[1,m],
                fill=None,
                mode='lines',
                name = 'ORD|REL',
                line_color='grey',
                line = dict(dash = 'dot'),
                ))
    
    #return fig
    
        
        
def plot_barcode_plotly(fig, barcode, filt_length):
    
    i = 1
    
    #fig = go.Figure()

    for bar in barcode:
        
        x = bar["interval"][0]
        y = bar["interval"][1]

        if bar["type"]=='ORD':
            
            fig.add_trace(go.Scatter(x=[x,y], y=[i,i],
                fill=None,
                mode='lines',
                name = '(I,'+str(bar['dimension'])+')',
                line_color='LightSkyBlue',
                showlegend=False
                ), row=1, col=1)
            fig.add_trace(go.Scatter(x=[y], y=[i],
                fill=None,
                mode='markers',
                name = '(I,'+str(bar['dimension'])+')',
                marker=dict(
                    color='LightSkyBlue',
                    size=8,
                    line=dict(
                        color='LightSkyBlue',
                        width=0.5
                    )
                ),
                showlegend=False
                ), row=1, col=1)
            fig.add_trace(go.Scatter(x=[x], y=[i],
                fill=None,
                mode='markers',
                name = '(I,'+str(bar['dimension'])+')',
                marker=dict(
                    color='LightSkyBlue',
                    size=8,
                    line=dict(
                        color='LightSkyBlue',
                        width=0.5
                    )
                ),
                showlegend=False
                ), row=1, col=1)
            
        elif bar["type"]=='REL':
            
            fig.add_trace(go.Scatter(x=[y+filt_length,x+filt_length], y=[i,i],
                fill=None,
                mode='lines',
                name = '(II,'+str(bar['dimension'])+')',
                line_color='aquamarine',
                showlegend=False
                ))
            fig.add_trace(go.Scatter(x=[x+filt_length], y=[i],
                fill=None,
                mode='markers',
                name = '(II,'+str(bar['dimension'])+')',
                marker=dict(
                    color='aquamarine',
                    size=8,
                    line=dict(
                        color='aquamarine',
                        width=0.5
                    )
                ),
                showlegend=False
                ), row=1, col=1)
            fig.add_trace(go.Scatter(x=[y+filt_length], y=[i],
                fill=None,
                mode='markers',
                name = '(II,'+str(bar['dimension'])+')',
                marker=dict(
                    color='aquamarine',
                    size=8,
                    line=dict(
                        color='aquamarine',
                        width=0.5
                    )
                ),
                showlegend=False
                ), row=1, col=1)
            
        elif bar["type"]=='EP+':
            
            fig.add_trace(go.Scatter(x=[x,y+filt_length], y=[i,i],
                fill=None,
                mode='lines',
                name = '(III,'+str(bar['dimension'])+')',
                line_color='cornflowerblue',
                showlegend=False
                ), row=1, col=1)
            fig.add_trace(go.Scatter(x=[x], y=[i],
                fill=None,
                mode='markers',
                name = '(III,'+str(bar['dimension'])+')',
                marker=dict(
                    color='cornflowerblue',
                    size=8,
                    line=dict(
                        color='cornflowerblue',
                        width=0.5
                    )
                ),
                showlegend=False
                ), row=1, col=1)
            fig.add_trace(go.Scatter(x=[y+filt_length], y=[i],
                fill=None,
                mode='markers',
                name = '(III,'+str(bar['dimension'])+')',
                marker=dict(
                    color='cornflowerblue',
                    size=8,
                    line=dict(
                        color='cornflowerblue',
                        width=0.5
                    )
                ),
                showlegend=False
                ), row=1, col=1)
            
        elif bar["type"]=='EP-':
            fig.add_trace(go.Scatter(x=[x+filt_length,y], y=[i,i],
                fill=None,
                mode='lines',
                name = '(IV,'+str(bar['dimension'])+')',
                line_color='violet',
                showlegend=False
                ), row=1, col=1)
            fig.add_trace(go.Scatter(x=[x+filt_length], y=[i],
                fill=None,
                mode='markers',
                name = '(IV,'+str(bar['dimension'])+')',
                marker=dict(
                    color='violet',
                    size=8,
                    line=dict(
                        color='violet',
                        width=0.5
                    )
                ),
                showlegend=False
                ), row=1, col=1)
            fig.add_trace(go.Scatter(x=[y], y=[i],
                fill=None,
                mode='markers',
                name = '(IV,'+str(bar['dimension'])+')',
                marker=dict(
                    color='violet',
                    size=8,
                    line=dict(
                        color='violet',
                        width=0.5
                    )
                ),
                showlegend=False
                ), row=1, col=1)
        i+=1
        
    fig['layout'].update({
        'showlegend': True,
        'width': 600,
        'height': 500,
    })
    fig.update_layout(
    xaxis_title="Filtration value",
    yaxis_title="Topological feature"
    )
    
    return fig