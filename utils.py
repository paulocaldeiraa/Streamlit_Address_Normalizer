import streamlit as st #pip install streamlit
import pandas as pd
from geopy.geocoders import Nominatim #pip install geopy
from geolocate import geolocate as geo
from geopy.point import Point

# ---------- Functions ----------
@st.experimental_memo
def get_coordinates(df):
# Use the import geo to get a coordinates from uplouaded file
    loc = []
    for address in df['Address']:
        loc.append(geo(address))
    df['Coordinates'] = loc

# Create a new DataFrame to better replace the useless string
    df.to_csv('geo_df.csv', index=False)
    df_geo = pd.read_csv('geo_df.csv')
    df_geo['Coordinates'].replace('latitude', '', regex=True,inplace=True)
    df_geo['Coordinates'].replace('longitude', '', regex=True,inplace=True)
    df_geo['Coordinates'].replace('{', '', regex=True,inplace=True)
    df_geo['Coordinates'].replace("''", '', regex=True,inplace=True)
    df_geo['Coordinates'].replace('}', '', regex=True,inplace=True)
    df_geo['Coordinates'].replace(':', '', regex=True,inplace=True)
    df_geo.to_csv('coords_df.csv', index=False)
    df_coords = pd.read_csv('coords_df.csv')

    return df_coords

@st.experimental_memo
def process_addresses(df):
    df_coords = pd.read_csv('coords_df.csv')
# Creating new columns to separate the address
    road = []
    house_number = []
    suburb = []
    city = []
    county = []
    state = []
    postcode = []
    country = []

# Using geo to get the full address from the coordinates
    for geoloc in df_coords['Coordinates']:
        geolocator = Nominatim(user_agent="AddressNormalizer")

        try:
            location = geolocator.reverse(geoloc)
            road.append(location.raw['address']['road'])
        except KeyError:
            road.append('None')
        except ValueError:
            road.append('None')

        try:
            location = geolocator.reverse(geoloc)
            house_number.append(location.raw['address']['house_number'])
        except KeyError:
            house_number.append('None')
        except ValueError:
            house_number.append('None')

        try:
            location = geolocator.reverse(geoloc)
            suburb.append(location.raw['address']['suburb'])
        except KeyError:
            suburb.append('None')
        except ValueError:
            suburb.append('None')

        try:   
            location = geolocator.reverse(geoloc)
            city.append(location.raw['address']['city'])
        except KeyError:
            city.append('None')
        except ValueError:
            city.append('None')

        try: 
            location = geolocator.reverse(geoloc)
            county.append(location.raw['address']['county'])
        except KeyError:
            county.append('None')
        except ValueError:
            county.append('None')

        try:
            location = geolocator.reverse(geoloc)
            state.append(location.raw['address']['state'])
        except KeyError:
            state.append('None')
        except ValueError:
            state.append('None')

        try:
            location = geolocator.reverse(geoloc)
            postcode.append(location.raw['address']['postcode'])
        except KeyError:
            postcode.append('None')
        except ValueError:
            postcode.append('None')

        try: 
            location = geolocator.reverse(geoloc)
            country.append(location.raw['address']['country'])
        except KeyError:
            country.append('None')
        except ValueError:
            country.append('None')


# Saving the result in each of the new columns 
    df_coords['Road'] = pd.DataFrame(road)
    df_coords['House_Number'] = pd.DataFrame(house_number)
    df_coords['Suburb'] = pd.DataFrame(suburb)
    df_coords['City'] = pd.DataFrame(city)                                                                   
    df_coords['County'] = pd.DataFrame(county)
    df_coords['State'] = pd.DataFrame(state)   
    df_coords['Postcode'] = pd.DataFrame(postcode)
    df_coords['Country'] = pd.DataFrame(country)
    df_coords.to_csv('final_df.csv', index = False)

    download_df = pd.read_csv('final_df.csv')

    return download_df


@st.cache
def convert_df(df):
# IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')