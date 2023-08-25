import streamlit as st
import base64
import streamlit.components.v1 as components
import stvis
from stvis import pv_static
from plotly.subplots import make_subplots
import numpy as np
import networkx as nx
from bijection import *

from helpers import cycle, complete, plot_diagram_plotly, threshold, graph_time_series
from visualization import plot_barcode_LZZ_plotly, plot_extended_barcode_plotly

def interactive_function_EP(space, filtration):

    s = gd.SimplexTree()
    for edge in eval(space):
        s.insert(edge)
    for filt in eval(filtration):
        s.assign_filtration(filt[0], filt[1])
    _ = s.make_filtration_non_decreasing()
    real_filtration = list(s.get_filtration())    
    s.extend_filtration()
    dgms = s.extended_persistence(min_persistence=1e-5)
    return dgms


def interactive_function_LZZ(space, filtration):
    
    s = gd.SimplexTree()
    for edge in eval(space):
        s.insert(edge)  
    for filt in eval(filtration):
        s.assign_filtration(filt[0], filt[1])
    _ = s.make_filtration_non_decreasing()
    real_filtration = list(s.get_filtration())  
    s.extend_filtration()
    dgms = s.extended_persistence(min_persistence=1e-5)
    B = EP_to_LZZ(real_filtration, dgms)
    return B


def interactive_barcodes():
    
    st.header('Computing barcodes')
    st.markdown('With this feature, you can choose your own space and filtration. Then, we compute the barcode of your choice with a simple method. More precisely, the extended persistence barcode (1) is computed via the GHUDI library, and the levelset zigzag persistence barcode is computed by applying the bijective mapping to barcode (1).')
    user_space = st.text_input("Choose a simplicial complex, as in the example below (default filtrated space) - e.g. add the edge [0,1] to your space.", [[0,1], [1,2], [1,3], [2,4], [3,4], [4,5], [2,6], [3,7], [4,7], [5,7], [1,8], [2,8], [1,9]])
    user_filtration = st.text_input("Choose a filtration, of the form below (default filtration) - e.g. assign to vertex [6] the value 0.5.", [([0],0),([1],1),([2],2),([3],3),([4],4),([5],5),([6],0.5),([7],4.5),([8],5),([9],6)])
    g = st.checkbox('Begin computation')

    if g:
        G = nx.Graph()
        for edge in eval(user_space):
            G.add_edge(*edge)
        with st.expander("See your simplicial complex."):
            time_series = graph_time_series(user_space, user_filtration)
            display_filt_complex(time_series)
        st.markdown("Now, you can choose between plotting diagrams or barcodes.")
        d = st.checkbox("Display persistence diagrams")
        b = st.checkbox("Display persistence barcodes")
        dgms = interactive_function_EP(user_space,user_filtration)
        B = interactive_function_LZZ(user_space,user_filtration)
        l,r = st.columns(2)
        filt = [v[1] for v in eval(user_filtration)]
        if d:
            fig_ = make_subplots(
                rows=2, cols=4,
                subplot_titles = ['Ordinary PD',
                                'Relative PD',
                                'Closed-open LZZ PD',
                                'Open-closed LZZ PD',
                                 'Extended+ PD',
                                 'Extended- PD',
                                 'Closed-closed LZZ PD',
                                 'Open-open LZZ PD'],
                                x_title = 'Birth',
                                y_title = "Death"
                )
            plot_diagram_plotly(fig_, dgms, filt, class_='extended')
            plot_diagram_plotly(fig_, dgms, filt, class_='levelset')
            fig_['layout'].update({
                'width': 1000,
                'height': 600,
            })
            st.plotly_chart(fig_)

        if b:
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles = ['Extended persistence barcode',
                                'Levelset zigzag persistence barcode']
                )
            plot_extended_barcode_plotly(fig, dgms, filt)
            plot_barcode_LZZ_plotly(fig, B)
            fig['layout'].update({
                'width': 1000,
                'height': 500,
            })
            st.plotly_chart(fig)
            bijection_explained()


def computing_barcodes():
    
    st.header('Computing barcodes')
    st.markdown('In this example, we consider fixed choices of space and filtration, based on symmetric graphs with natural height functions. Then, we compute the barcode of your choice with a simple method. The extended persistence barcode (1) is computed via GHUDI, and the levelset zigzag persistence barcode is computed by applying the bijective mapping to barcode (1).')
    st.markdown('This feature is essentially designed to allow for better intuition on how extended persistence and levelset zigzag barcodes behave, through working with simple simplicial complexes and height functions as filtrating tools.')

    choice = st.selectbox('What space do you want to look at?', ('The circle as a 6-cycle', 
                                         'The complete graph on 8 nodes'))
    go = st.checkbox('Begin computation')
    if go:
        if choice == 'The circle as a 6-cycle':
            trio = cycle()   
            space = trio[0]
            filtration = trio[1]
            G = trio[2]
        elif choice == 'The complete graph on 8 nodes':     
            trio_ = complete() 
            space = trio_[0]
            filtration = trio_[1]
            G = trio_[2]
        with st.expander("See your simplicial complex."):
            time_series = graph_time_series(space, filtration)   
            display_filt_complex(time_series)
        dgms = interactive_function_EP(space,filtration)
        B = interactive_function_LZZ(space,filtration)
        d = st.checkbox("Display persistence diagrams")
        b = st.checkbox("Display persistence barcodes")
        filt = [v[1] for v in eval(filtration)]
        if d:  
            fig_ = make_subplots(
                rows=2, cols=4,
                subplot_titles = ['Ordinary PD',
                                'Relative PD',
                                'Closed-open LZZ PD',
                                'Open-closed LZZ PD',
                                 'Extended+ PD',
                                 'Extended- PD',
                                 'Closed-closed LZZ PD',
                                 'Open-open LZZ PD'],
                                x_title = 'Birth',
                                y_title = "Death"
                )
            plot_diagram_plotly(fig_, dgms, filt, class_='extended')
            plot_diagram_plotly(fig_, dgms, filt, class_='levelset')
            fig_['layout'].update({
                'width': 1000,
                'height': 600,
            }) 
            st.plotly_chart(fig_)
        if b:      
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles = ['Extended persistence barcode',
                                'Levelset zigzag persistence barcode']
                )
            
            plot_extended_barcode_plotly(fig, dgms, filt)
            plot_barcode_LZZ_plotly(fig, B)
            fig['layout'].update({
                'width': 1000,
                'height': 500,
            })
            
            st.plotly_chart(fig)


def bijection_vis():
    
    st.header("A simple example")
    st.sidebar.header("Bijection visualization")
    st.markdown("#### Visualizing the bijection of intervals between levelset zigzag and extended barcodes.")
    st.markdown("")
    __left,__right = st.columns(2) 
    #__left.image("../figures/bij_viz1.png")
    #__right.image("../figures/bij_viz2.png")
    st.image('../figures/bijection.png', caption = 'Interval bijection example.')
    with st.expander("See explanation"): 
        st.write("""Barcodes of levelset zigzag persistence and extended persistence are denoted by $\mathbb{B}_{LZZ}$ and $\mathbb{B}_{EP(+)}$ respectively. In the extended persistence barcode, the central vertical segment separates points living in $\mathbb{R}$ from points living in $\mathbb{R}^\circ=(\mathbb{R},\geq)$. Intervals of the same color are in correspondence via the bijective mapping. We provide an instance of the mapping for each type of intervals (there are four in total).
        """)
        

def display_filt_complex(time_series):
    
    values = [v[1] for v in time_series]
    graphs = [v[0] for v in time_series]
    t = st.slider("Filtration threshold", min(values), max(values), max(values))
    index = values.index(t)
    pv_static(graphs[index])


def description():
    
    st.header('Introduction')
    st.markdown('Hey there! This app is developped in the context of a project done by [Nicolas Berkouk](https://people.epfl.ch/nicolas.berkouk) and [Luca Nyckees](https://github.com/LucaNyckees) at EPFL, within the *Laboratory for Topology and Neuroscience*.')
    st.header('Context')
    st.markdown("Topological data analysis is a branch in the field of applied mathematicsthat has rapidly grown in the past few years. It offers toolboxes to study theshape of data and finds applications in various domains of machine learning.Key concepts in topological data analysis are the notion ofpersistent homology and its extended versions, namely extended persistent homology and zigzag homology, which offer a way of analysing the behavior of topological features along a diagram of spaces built from data.")
    st.header('Description')
    st.markdown('Zigzag persistence, as introduced by Carlsson and De Silva, offers a way to better understand the behavior of topological features observed in a family of spaces or pointclouds by generalizing the setting of persistent homology. An interesting case is the one of *levelset zigzag persistence*, that encodes more information than standard persistence and offers an alternative intuition to extended persistence. A bijection between the extended persistence barcode and the zigzag barcode can be established via so-called "diamond moves", involving the presence of relative Mayer-Vietoris diamonds, illustrated in the animation below. ')
    #st.markdown("![Alt Text](https://github.com/LucaNyckees/ParametricMorseTheory/blob/main/pyramid_zigzag.gif)")
    _left, _right = st.columns(2)
    # with _right: 
        # st.image("../figures/pyramid_zigzag.gif")   
    st.image("../figures/pipeline.png", caption='General pipeline', use_column_width='auto')
    st.markdown('The precise statement is formulated as the Strong Diamond Principle - sometimes called the Pyramid Theorem. The whole process relies on consecutive transformations between two sequences of spaces that differ only at one point, so that the difference can be expressed by a relative Mayer-Vietoris diamond.')
    #st.markdown("""In the animated diagram above, we consider a function $f\in \mathrm{Map}(\mathbb{X},\mathbb{R})$ and look at the spaces defined as $\mathbb{X}_i^j = f^{-1}([s_i,s_j]),$ where the values $s_k$ are regular values of the pair $(\mathbb{X},f)$. If follows that here, all arrows are inclusions of spaces.
    #            """)
    st.header('Our Goal')
    st.markdown('In this project, we aim at providing a tool to compute levelset zigzag persistence. We deduce the results from computations on extended persistence, which are already implemented in C++. To this end, we make use of Python bindings. This way, we develop an efficient computational tool to add to the general data science toolbox.')    
    st.header('Key-concepts')
    st.markdown("""
        * zigzag persistence \n 
        * extended persistence \n
        * barcodes \n
        * strong diamond principle \n
        * relative Mayer-Vietoris diamonds \n
        * pyramid theorem \n 
        * combinatorial bijective mapping
        """)
    
    
def whole_story():
    
    main()
    
    with open("../reports/report.pdf", "rb") as file:
        btn = st.sidebar.download_button(
            label="Download report",
            data=file,
            file_name="report.pdf",
            mime="report/pdf"
        )
        
        
def references():
    
    st.title("Related articles and references")
    st.subheader("We give a list of the main references and articles linked to this project.")
    st.write("You can choose an article here and read it!")
    
    elt = st.selectbox('What article do you want to see?', ('Zigzag Persistence', 
                                             'Structure and Interleavings of Relative Interlevel Set Cohomology',
                                             'Zigzag Persistent Homology and Real-valued Functions',
                                             'Computing Optimal Persistent Cycles for Levelset Zigzag on Manifold-like Complexes'))
    
    if elt == 'Zigzag Persistence':
        
        reference('../articles/FODAVA-08-03.pdf')
        
    elif elt == 'Structure and Interleavings of Relative Interlevel Set Cohomology':
        
        reference('../articles/interlevelsets_magnus.pdf')
        
    elif elt == 'Zigzag Persistent Homology and Real-valued Functions':
        
        reference('../articles/morozov.pdf')
        
    elif elt == 'Computing Optimal Persistent Cycles for Levelset Zigzag on Manifold-like Complexes':
        
        reference('../articles/tamal_dey.pdf')
        
         
def github():
    st.sidebar.markdown("The entire code of the project, from source code to notebooks, is available at our GitHub repo [here](https://github.com/LucaNyckees/zigzag). Have a look!")
        
        
def contacts():
    st.sidebar.markdown("""
        * Luca Nyckees ([EPFL](https://people.epfl.ch/luca.nyckees), [GitHub](https://github.com/LucaNyckees))\n
        * Nicolas Berkouk [EPFL](https://people.epfl.ch/nicolas.berkouk), [Site](https://nberkouk.github.io/)
        """)
    
    
def main():
    
    st.title("The Whole Story")
    st.subheader("This is the project report, containing all the details of our data analysis.")
    st.write("You have the possibility to download it - to do this, please check the sidebar.")
    with open("../reports/report.pdf","rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)
    
    
def reference(file):
    with open(file,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
        
    st.markdown(pdf_display, unsafe_allow_html=True)
    
    
def bijection_explained():
    
    with st.expander("See explanation"):
        st.markdown("The one-to-one correspondence between extended persistence intervals and levelset zigzag intervals in the barcodes above can is drawn from the bijection below, introduced in [[1]](https://www.mrzv.org/publications/zigzags/socg09/).")
        st.latex(r'''
\text{Type I : } [a_i,a_j)\leftrightarrow [a_i,a_j)\\
\text{Type II : } [\bar{a}_j,\bar{a}_i)^+\leftrightarrow (a_i,a_j]\\
\text{Type III : } [a_i,\bar{a}_j)\leftrightarrow [a_i,a_j]\\
\text{Type IV : } [a_j,\bar{a}_i)^+\leftrightarrow (a_i,a_j)
        ''')
        st.markdown("This is a bijective mapping that preserves the homological dimension of features in most cases, with exceptional degree-shifts of $\pm 1$. On the left, we have the intervals appearing in the extended persistence barcode and their mapped version as levelset zigzag persistence interals on the right. Here, the bar symbol on a value $a_i$ denotes the copy of the critical value $a_i$ in the opposite real line, corresponding to the relative homology case. In other words, what we do is extend the basic input filtration $T = [t_1,t_2]$ to an extended filtration $$E(T) = [t_1,t_2]\cup [t_2,2t_2-t_1]$$ and define")
        st.latex(r'''\bar{t}=t+t_2-t_1 \text{ for any } t\in [t_1,t_2].''')
        
