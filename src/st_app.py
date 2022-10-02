import streamlit as st
import matplotlib
from st_utils import *
from bijection import *

plt.style.use('fivethirtyeight')
matplotlib.rcParams.update({'font.size': 10})

st.set_page_config(layout='wide')
st.markdown("<h1 style='text-align: center;'> Computing Levelset Zigzag Homology</h1>",
            unsafe_allow_html=True)
MODES = ['Choose your data', 'Fixed graphs', 'Barcode bijection']
st.sidebar.header('Options')
INFO = st.sidebar.radio("Content",('Project description', 'Interactive part'))

if INFO == 'Project description':
    description()
elif INFO == 'Interactive part':
    SELECTED_MODE = st.sidebar.selectbox("Visualization mode", MODES, index=0)
    if SELECTED_MODE == MODES[0]:
        interactive_barcodes()
    elif SELECTED_MODE == MODES[1]:
         computing_barcodes()
    elif SELECTED_MODE == MODES[2]: 
        bijection_vis()

if st.sidebar.button("GitHub"):
    github()
if st.sidebar.button("Contacts"):
    contacts()
    

                