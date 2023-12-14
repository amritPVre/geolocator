# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 11:10:20 2023

@author: amrit
"""

import streamlit as st
from geopy.geocoders import Nominatim
import pydeck as pdk


geolocator = Nominatim(user_agent="geoapiExercises")

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
import yfinance as yf
import streamlit as st
import plotly.graph_objects as go

# Title of the app
st.title('Live Stock Data with Candlestick Chart from Yahoo Finance')

# Input fields for user input
ticker = st.text_input('Enter the stock ticker symbol (e.g., IREDA.NS):')
period = st.selectbox('Select the period:', ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'))
interval = st.selectbox('Select the interval:', ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'))

# Button to fetch the data
if st.button('Fetch Data'):
    if ticker:
        with st.spinner('Fetching data...'):
            data = yf.download(tickers=ticker, period=period, interval=interval)
            st.write(f"Displaying {interval} candlestick chart for {ticker}")
            
            # Check if data is empty
            if not data.empty:
                # Candlestick chart
                fig = go.Figure(data=[go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name='Candlestick')])
                
                # Update the layout
                fig.update_layout(
                    title='Candlestick Chart',
                    yaxis_title='Stock Price',
                    xaxis_title='Date'
                )
                
                # Display the candlestick chart
                st.plotly_chart(fig, use_container_width=True)
                
                # Display the latest 50 data rows in a tabular format
                st.write("Latest 50 Data Rows:")
                st.dataframe(data.tail(50))  # Show the last 50 rows of the dataframe
            else:
                st.error('No data found for the selected ticker.')
    else:
        st.error('Please enter a stock ticker symbol.')

#
