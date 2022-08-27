# Import the package
import streamlit as st #pip install streamlit
import pandas as pd
import numpy as np
import geopy #pip install geopy
from geopy.geocoders import Nominatim
import geolocate as geo
# from geolocate import geolocate as geo #pip install geolocate


# ---------- Prepare the DataFrame ----------

file_name = st.file_uploader("Choose a file")

df = pd.read_csv(file_name, low_memory=False)

# ---------- Streamlit Functions ----------

st.sidebar.number_input('Teste')
st.write('Olá Paulo, apenas conferindo se está tudo ok!! ')

st.sidebar.number_input('teste2')

