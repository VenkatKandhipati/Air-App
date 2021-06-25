#Venkat Kandhipati (Student ID: 78919110)
import json
import urllib.parse
import urllib.request
import time

"""
ReverseGeocodeNominatim Interface

A 'ReverseGeocodeNominatim' is an object that can extract JSON data using the 
given specific input which would be the same for all these methods. 

interface ReverseGeocodeNominatim():

    def extract_data(self, var): # a function that takes in one arguement as a string
    which will get the JSON data of the input given.

"""

BASE_NOMINATIM_URL = "https://nominatim.openstreetmap.org"

class ReverseGeocodeNominatimAPI():
    '''Class used when the input for the reverse nominatim is through an API request.'''
    def extract_data(self, lat_lon: tuple) -> dict:
        '''Extract the JSON data from the nominatim api using the lat/lon passed in and return the data as a dictionary.'''
        full_url = BASE_NOMINATIM_URL + '/reverse?' + urllib.parse.urlencode([('lat', str(lat_lon[0])), ('lon', str(lat_lon[1])), ('format', 'json')])
        
        response = None
        time.sleep(2)
        try:
            request = urllib.request.Request(full_url)
            request.add_header('Referer', 'vkandhip@uci.edu')
            response = urllib.request.urlopen(request)
            json_text = response.read().decode(encoding = 'utf-8')
        except urllib.error.HTTPError as e:
            print('FAILED')
            print(f'{e.code} {full_url}')
            print('NOT 200')
            quit()
        except urllib.error.URLError as e:
            print('FAILED')
            print(f'{full_url}')
            print('NETWORK')
            quit()
        except json.decoder.JSONDecodeError:
            print('FAILED')
            print(f'200 {full_url}')
            print('FORMAT')
            quit()
        finally:
            if response != None:
                response.close()
        
        return json.loads(json_text)

class ReverseGeocodeNominatimFile():
    '''Class used when the input for the reverse nominatim is through a file.'''
    def extract_data(self, path: str) -> dict:
        f = None
        try:
            f = open(path, 'r')
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


def parse_reversenominatim_input(reverse_n_input: str, max_sensors: int, final_sensor_data: list) -> tuple:
    '''Parse the given input string to decide to make a an API or File ReverseNominatim object.'''
    if 'NOMINATIM' in reverse_n_input:
        extract_param = []
        class_lst = []
        for data in final_sensor_data:
            class_lst.append(ReverseGeocodeNominatimAPI())
            extract_param.append((data[1], data[2]))

    elif 'FILES' in reverse_n_input:
        path = reverse_n_input.split(' ', 1 + max_sensors)
        extract_param = path[2:]
        # print(path)
        class_lst = []
        for p in extract_param:
            class_lst.append(ReverseGeocodeNominatimFile())

   
    addresses = []
    for i in range(len(final_sensor_data)):
        dict_results = class_lst[i].extract_data(extract_param[i])
        addresses.append(dict_results['display_name'])
    
    return addresses
    
    
