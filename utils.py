
import streamlit as st #pip install streamlit
import pandas as pd
import geopy #pip install geopy
from geopy.geocoders import Nominatim
from geolocate import geolocate as geo


# ---------- Functions ----------


def get_coordenates(df):
# Use the import geo to get a coordinates from uplouaded file
    loc = []
    for address in df['Address']:
        loc.append(geo(address))
    df['Coordinates'] = loc

# Create a new DataFrame to better replace the useless string
    df.to_csv('new_df.csv', index = False)
    df_geo = pd.read_csv('new_df.csv')
    df_geo['Coordinates'].replace('latitude', '', regex=True,inplace=True)
    df_geo['Coordinates'].replace('longitude', '', regex=True,inplace=True)
    df_geo['Coordinates'].replace('{', '', regex=True,inplace=True)
    df_geo['Coordinates'].replace("''", '', regex=True,inplace=True)
    df_geo['Coordinates'].replace('}', '', regex=True,inplace=True)
    df_geo['Coordinates'].replace(':', '', regex=True,inplace=True)
    df_geo.to_csv('new_df.csv', index = False)
    df_coordinates = pd.read_csv('new_df.csv')

    return df_coordinates


def split_address(df):
# Read the new dataframe created from the uploaded file
    df_coordinates = pd.read_csv('new_df.csv')

# Creating new columns to separate the address
    locator = Nominatim(user_agent="myGeocoder")
    dic_road = []
    dic_house_number = []
    dic_suburb = []
    dic_city = []
    dic_county = []
    dic_state = []
    dic_postcode = []
    dic_country = []

# Using geo to get the full address from the coordinates
    for geoloc in df_coordinates['Coordinates']:
        location = locator.reverse(geoloc)

        try:
            dic_road.append(location.raw['address']['road'])
        except KeyError:
            dic_road.append('None')

        try:
            dic_house_number.append(location.raw['address']['house_number'])
        except KeyError:
            dic_house_number.append('None')

        try:
            dic_suburb.append(location.raw['address']['suburb'])
        except KeyError:
            dic_suburb.append('None')

        try:   
            dic_city.append(location.raw['address']['city'])
        except KeyError:
            dic_city.append('None')

        try: 
            dic_county.append(location.raw['address']['county'])
        except KeyError:
            dic_county.append('None')

        try:
            dic_state.append(location.raw['address']['state'])
        except KeyError:
            dic_state.append('None')

        try:
            dic_postcode.append(location.raw['address']['postcode'])
        except KeyError:
            dic_postcode.append('None')

        try: 
            dic_country.append(location.raw['address']['country'])
        except KeyError:
            dic_country.append('None')
            
# Saving the result in each of the new columns 
    df_coordinates['Road'] = pd.DataFrame(dic_road)
    df_coordinates['House_Number'] = pd.DataFrame(dic_house_number)
    df_coordinates['Suburb'] = pd.DataFrame(dic_suburb)
    df_coordinates['City'] = pd.DataFrame(dic_city)                                                                   
    df_coordinates['County'] = pd.DataFrame(dic_county)
    df_coordinates['State'] = pd.DataFrame(dic_state)
    df_coordinates['Postcode'] = pd.DataFrame(dic_postcode)
    df_coordinates['Country'] = pd.DataFrame(dic_country)
    df_coordinates.to_csv('to_be_downloaded.csv', index = False)

    download_df = pd.read_csv('to_be_downloaded.csv')

    return download_df


@st.cache
def convert_df(df):
# IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')