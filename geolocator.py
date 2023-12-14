# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 11:10:20 2023

@author: amrit
"""

import streamlit as st
from geopy.geocoders import Nominatim
import pydeck as pdk


geolocator = Nominatim(user_agent="geolocator-pv.streamlit.app")

st.title('Country/Region Coordinate Finder')
place = st.text_input('Enter a country or region:')

if st.button('Get Coordinates'):
    location = geolocator.geocode(place)
    if location:
        st.write(f"Coordinates of {place}:")
        st.write(f"Latitude: {location.latitude}, Longitude: {location.longitude}")

        # Create a map
        map = pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state={
                'latitude': location.latitude,
                'longitude': location.longitude,
                'zoom': 11,
                'pitch': 50,
            },
            layers=[
                pdk.Layer(
                   'ScatterplotLayer',
                   data=[{'position': [location.longitude, location.latitude], 'size': 100}],
                   get_position='position',
                   get_color=[255, 0, 0, 200],
                   get_radius='size',
                ),
            ],
        )
        st.pydeck_chart(map)

    else:
        st.write("Location not found. Please try again.")


#-----------------------

st.write('_______')
