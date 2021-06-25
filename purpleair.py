#Venkat Kandhipati (Student ID: 78919110)
import math
import json
import urllib.parse
import urllib.request
import time

"""
PurpleAir Interface

A 'PurpleAir' is an object that can extract JSON data using the 
given specific input which would be the same for all these methods. 

interface PurpleAir():

    def extract_data(self, var: str): # a function that takes in one arguement as a string
    which will get the JSON data of the input given.

"""

class PurpleAirAPI():
    '''Class used when the input for the AQI information is through an API request.'''
    def extract_data(self, url: str) -> dict:
        '''Extract the JSON data from the PurpleAir api and return the data as a dictionary.'''
        response = None
        try:
            time.sleep(2)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding = 'utf-8')
        except urllib.error.HTTPError as e:
            print('FAILED')
            print(f'{e.code} {url}')
            print('NOT 200')
            quit()
        except urllib.error.URLError as e:
            print('FAILED')
            print(f'{url}')
            print('NETWORK')
            quit()
        except json.decoder.JSONDecodeError:
            print('FAILED')
            print(f'200 {url}')
            print('FORMAT')
            quit()
        finally:
            if response != None:
                response.close()

        return json.loads(json_text)

class PurpleAirFile():
    '''Class used when the input for the AQI information is through a file.'''
    def extract_data(self, path: str) -> dict:
        f = None
        try:
            f = open(path, encoding='utf-8')
            contents = f.read()
            data = json.loads(contents)
        except FileNotFoundError:
            print('FAILED')
            print(path)
            print('MISSING')
            quit()
        except json.decoder.JSONDecodeError:
            print('FAILED')
            print(path)
            print('FORMAT')
            quit()
        finally:
            if f != None:
                f.close()
        
        return data

def parse_purple_air(AQI_info_input: str) -> dict:
    '''Take the input given and parse it to decide if we need to request the API or use file. Then return a dictionary of the purpleair data.'''
    if 'PURPLEAIR' in AQI_info_input:
        extract_param = 'https://www.purpleair.com/data.json'
        purpleair_data = PurpleAirAPI()
    elif 'FILE' in AQI_info_input:
        extract_param = AQI_info_input.split(' ', 2)[-1]
        purpleair_data = PurpleAirFile()

    dict_results = purpleair_data.extract_data(extract_param)
    return dict_results

def filter_data(data_dict: dict, radius_range: float, center: tuple, aqi_threshold: float, max_locations: int) -> list:
    '''Take the input dictionary and filter out all the sensors that are in the given range.'''
    data = data_dict['data']
    
    final_sensors = []
    for sensor in data:
        if sensor[25] == 0 and sensor[1] != None and sensor[27] != None and sensor[28] != None and sensor[4] <= 3600: #Check if the sensor is outdoor and pm not null
            pm = sensor[1]
            lat = sensor[27]
            lon = sensor[28]
            distance = equirectangular_approximation((float(lat), float(lon)), center)
            aqi = calc_AQI(pm)

            if distance <= radius_range and aqi >= aqi_threshold:
                final_sensors.append([pm, lat, lon, distance, aqi])

    
    final_sensors.sort(key = get_aqi, reverse = True)
    final_sensors = final_sensors[0:max_locations]
    return final_sensors

        
def get_aqi(sensor: list) -> float:
    '''Used to sort the sensors list based on their aqi.'''
    return sensor[-1]

def equirectangular_approximation(point1: tuple, point2: tuple) -> float:
    '''Approximate the distance between two points given by their longitudes and latitudes as a tuple.'''
    dlat = math.fabs(math.radians(point1[0]) - math.radians(point2[0]))
    dlon = math.fabs(math.radians(point1[1]) - math.radians(point2[1]))
    alat = (math.fabs(math.radians(point1[0]) + math.radians(point2[0]))) / 2
    radius = 3958.8

    x = (dlon) * (math.cos(alat))
    d = (math.sqrt((x**2) + (dlat**2))) * radius

    return d

def calc_AQI(pm: float) -> int:
    '''Calculate the AQI value based on the PM2.5 value passed in.'''
    if 0 <= pm < 12.1:
        if pm == 0:
            return 0
        elif pm == 12:
            return 50
        else:
            return (pm/12)*50
    elif 12.1 <= pm < 35.5:
        if pm == 12.1:
            return 51
        elif pm == 35.4:
            return 100
        else:
            return (((pm-12.1)/23.3) * 49) + 51
    elif 35.5 <= pm < 55.5:
        if pm == 35.5:
            return 101
        elif pm == 55.4:
            return 150
        else:
            return (((pm-35.5)/19.9) * 49) + 101
    elif 55.5 <= pm < 150.5:
        if pm == 55.5:
            return 151
        elif pm == 150.4:
            return 200
        else:
            return (((pm-55.5)/94.9) * 49) + 151
    elif 150.5 <= pm < 250.5:
        if pm == 150.5:
            return 201
        elif pm == 250.4:
            return 300
        else:
            return (((pm-150.5)/99.9) * 99) + 201
    elif 250.5 <= pm < 350.5:
        if pm == 250.5:
            return 301
        elif pm == 350.4:
            return 400
        else:
            return (((pm-250.5)/99.9) * 99) + 301
    elif 350.5 <= pm < 500.5:
        if pm == 350.5:
            return 401
        elif pm == 500.4:
            return 500
        else:
            return (((pm-350.5)/149.9) * 99) + 401
    elif pm >= 500.5:
        return 501
    


