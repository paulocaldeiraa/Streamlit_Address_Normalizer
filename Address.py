# Import the package
from ast import With
from functools import cache
from multiprocessing import Value
from multiprocessing.resource_sharer import stop
from operator import index
import streamlit as st #pip install streamlit
import pandas as pd
from geopy.geocoders import Nominatim #pip install geopy
from geolocate import geolocate as geo #pip install geolocate
from utils import process_addresses
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
st.write("Using an address it is possible to get the geographical coordinates \
     and the separation between street, city, neighborhood, and other fields. \
     Just upload a CSV, note that the column with the addresses needs to be named \
     'Address'. Don't worry if the addresses are not correct, the AN will correct \
     them for you. *This process may take a few minutes depending on the CSV*")

# ---------- Download Sample CSV ----------
csv = convert_df(pd.read_csv('st_address_sample.csv'))

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
    try:
        df = pd.read_csv(uploaded_file, low_memory=False)
        with col1:
# # Create the selected bottuns
            get_geo_button = st.button('Process the Addresses')  
            st.write(df)

 # ---------- Generate the Coordinates ----------

        if get_geo_button is True:
            with col3:
                process_addresses(df)
                csv = convert_df(pd.read_csv('final_df.csv'))

                st.download_button(
                    label="Download the CSV File",
                    data=csv,
                    file_name='Address_Normalizer_'+ \
                    datetime.now().strftime("%Y%m%d_%H%M") + '.csv',
                    mime='text/csv'
                )
                st.write(pd.read_csv('final_df.csv'))

 # ---------- Remove extra files ----------

        if os.path.exists("geo_df.csv"):
            os.remove("geo_df.csv")

        if os.path.exists("final_df.csv"):
            os.remove("final_df.csv")
        
    except UnicodeDecodeError:
        st.error('Please select a CSV file to proced.', icon="🚨")
    except FileNotFoundError:
        with col3:
            st.error('Please reselect the file, \
                 if the error continues please contact us.')