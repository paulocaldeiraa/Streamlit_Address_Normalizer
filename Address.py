# Import the package
from ast import With
from functools import cache
from multiprocessing import Value
from operator import index
import streamlit as st #pip install streamlit
import pandas as pd
import geopy #pip install geopy
from geopy.geocoders import Nominatim
# import geolocate
from geolocate import geolocate as geo #pip install geolocate
from utils import get_coordenates
from utils import split_address
from utils import convert_df
from datetime import datetime, timedelta
import os

# ---------- Page Config ----------
st.set_page_config(
     page_title="Address Normalizer",
     page_icon="🗺️",
     layout="wide",
     initial_sidebar_state="collapsed",
     menu_items={
         'Get Help': 'https://github.com/paulocaldeiraa/st_address_normalize',
         'Report a bug': "https://github.com/paulocaldeiraa/st_address_normalize",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )

# Setting the text instructions for the app 
st.title('🗺️ Address Normalizer')
st.header('📖 Instructions')
st.write("Using an address it is possible to obtain the geographical \
coordinates and the separation between street, city, neighborhood, \
and other fields. Just send a CSV, \
note that the column with the addresses needs to be named 'Address'. \
Don't worry if the addresses are not correct, the AN will correct it for you.")

# ---------- Download Sample CSV ----------
csv = convert_df(pd.read_csv('sample_csv.csv'))

st.download_button(
    label="Download sample CSV",
    data=csv,
    file_name='Address_Normalizer_Sample_'+ \
    datetime.now().strftime("%Y%m%d_%H%M") + '.csv',
    mime='text/csv'
)

# Create the field to input file
uploaded_file = st.file_uploader("Choose a CSV file")

# Defined the columns for customize layout
col1, col2, col3= st.columns([2,0.3,3])


# ---------- DataFrame ----------

if uploaded_file is not None:
# Define the DataFrame
    df = pd.read_csv(uploaded_file, low_memory=False)

    with col1: 
# Create the selected bottuns
        get_geo_button = st.button('Get Coordinates')  
        split_button = st.button('Split Address')  
        st.write(df)
        

 # ---------- Generate the Coordinates ----------
    if get_geo_button is True:
        with col3:
            get_coordenates(df)
            csv = convert_df(pd.read_csv('new_df.csv'))

            st.download_button(
                label="Download CSV with Coordinates",
                data=csv,
                file_name='Address_Normalizer_'+ \
                datetime.now().strftime("%Y%m%d_%H%M") + '.csv',
                mime='text/csv'
            )
            st.title('')
            st.write(get_coordenates(df))


    if split_button is True:
        with col3:
            split_address(df)
            csv = convert_df(pd.read_csv('to_be_downloaded.csv'))

            st.download_button(
                label="Download CSV with Splited Addresses",
                data=csv,
                file_name='Address_Normalizer_'+ \
                datetime.now().strftime("%Y%m%d_%H%M") + '.csv',
                mime='text/csv',
            )
            st.title('')
            st.write(split_address(df))

 # ---------- Remove extra files ----------
            if os.path.exists("new_df.csv"):
                os.remove("new_df.csv")

            if os.path.exists("to_be_downloaded.csv"):
                os.remove("to_be_downloaded.csv")
