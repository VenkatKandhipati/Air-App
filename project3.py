#Venkat Kandhipati (Student ID: 78919110)
from numpy import add
import nominatim, purpleair, reverse_nominatim
import math
import urllib
import json
import streamlit as st
import pandas as pd
import time
from PIL import Image


def lat_lon_printer(lat_lon: tuple) -> None:
    '''Print the latitiude and longitude with the added directions.'''
  
    if float(lat_lon[0]) >= 0:
        print(f"{lat_lon[0]}/N", end=' ')
    elif float(lat_lon[0]) < 0:
        print(f"{lat_lon[0][1:]}/S", end=' ')

    if float(lat_lon[1]) >= 0:
        print(f"{lat_lon[1]}/E", end='')
    elif float(lat_lon[1]) < 0:
        print(f"{lat_lon[1][1:]}/W", end='')
    print()
    
def rounding(AQI: float) -> int:
    '''Round the AQI to the nearest integer.'''
    if float(AQI) == int(AQI):
        return AQI
    elif float(str(AQI - int(AQI))[1:]) == 0.5:
        return math.ceil(AQI)
    else:
        return round(AQI)

def print_final_output(num: int, center: tuple, final_sensor_data: list, locations: list) -> None:
    '''Take all the data generated and print it in a friendly manner.'''
    print('CENTER', end=' ')
    lat_lon_printer(center)
    
    for i in range(num):
        print(f'AQI {rounding(final_sensor_data[i][-1])}')
        lat_lon_tuple = (str(final_sensor_data[i][1]), str(final_sensor_data[i][2]))
        lat_lon_printer(lat_lon_tuple)
        print(locations[i])

def run() -> None:
    '''Framework of the program.'''

    center = input()
    radius_range = float(input().split()[-1])
    threshold_aqi = float(input().split()[-1])
    max_locations = int(input().split()[-1])
    purple_air_input = input()
    nominatim_input = input()


    lat_lon = nominatim.parse_center(center)
    final_sensor_data = purpleair.filter_data(purpleair.parse_purple_air(purple_air_input), radius_range, (float(lat_lon[0]), float(lat_lon[1])), threshold_aqi, max_locations)
    addresses = reverse_nominatim.parse_reversenominatim_input(nominatim_input, max_locations, final_sensor_data)
    print_final_output(len(addresses), lat_lon, final_sensor_data, addresses)

def strun():
    st.set_page_config(
        page_title="Air Quality App",
        page_icon=":cloud:",
        layout="wide",
        initial_sidebar_state="expanded",)

    st.write("""
    # Hello!
    ## If you would like to know if there are any "hotspots" with bad air quality near you, please enter your location below.
    """)
    image = Image.open('AQI.jpg')
    st.sidebar.markdown('''
    # What is AQI? :cloud:
    ### AQI stands for Air Quality Index which is a commonly used measure for air pollution levels.
    ''')
    st.sidebar.write('')
    st.sidebar.write('\n\nThe higher the level :arrow_right: the greater the health concern :skull:')
    st.sidebar.image(image, caption='AQI readings chart')
    center = st.text_input(f'Enter location here')
    return center

def strunnext(center):
    if center != '':
        center = 'CENTER NOMINATIM ' + center
        radius_range = 200
        threshold_aqi = 50
        max_locations = 3
        purple_air_input = 'AQI PURPLEAIR'
        nominatim_input = 'REVERSE NOMINATIM'


        
        my_bar = st.progress(0)
        # for percent_complete in range(100):
        #     my_bar.progress(percent_complete + 1)
    # st.write(f'waiting{center}')
        lat_lon = nominatim.parse_center(center)
        my_bar.progress(25)
        try:
            final_sensor_data = purpleair.filter_data(purpleair.parse_purple_air(purple_air_input), radius_range, (float(lat_lon[0]), float(lat_lon[1])), threshold_aqi, max_locations)
        except:
            my_bar.progress(100)
            st.error('An Error occurred on our end, please refresh the page and try again.')
            st.stop()
        my_bar.progress(50)
        addresses = reverse_nominatim.parse_reversenominatim_input(nominatim_input, max_locations, final_sensor_data)
        my_bar.progress(100)
        print(final_sensor_data)
        aqi_values = [int(final_sensor_data[i][-1]) for i in range(len(addresses))]
        distance_values = [int(final_sensor_data[i][-2]) for i in range(len(addresses))]

        # st.balloons()
        print(addresses)

        # st.markdown(f'''
        # | Address | AQI |
        # | --- | ----------- |
        # | {addresses} | {aqi_values} |
        # | Paragraph | Text |
        
        # ''')

        # st.success('Done')
        # df = pd.DataFrame({
        #     'address': addresses,
        #     'AQI': aqi_values

        # })
        # st.dataframe(df)
        st.markdown('''
        ### Here are the locations with bad air quality near you. Refer to the sidebar to see how the AQI Values range.
        ''')
        for i in range(len(addresses)):
            st.markdown(f'''
            `{addresses[i]}`

                AQI: {aqi_values[i]}
                Distance from you: {distance_values[i]} miles

            ''')
            # st.write('AQI: ', final_sensor_data[i][0], ' Location: ', addresses[i])
            #AQI: {final_sensor_data[i][-1]}
        
if __name__ == '__main__':
    center = strun()
    print(center)
    strunnext(center)
