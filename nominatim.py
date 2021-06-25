#Venkat Kandhipati (Student ID: 78919110)
import json
import urllib.parse
import urllib.request
import time


BASE_NOMINATIM_URL = "https://nominatim.openstreetmap.org"

"""
ForwardGeocodeNominatim Interface

A 'ForwardGeocodeNominatim' is an object that can extract JSON data using the 
given specific input which would be the same for all these methods. 

interface ForwardGeocodeNominatim():

    def extract_data(self, var: str): # a function that takes in one arguement as a string
    which will get the JSON data of the input given.

"""
class ForwardGeocodeNominatimAPI():
    '''Class used when the input for the center is through an API request.'''
    def extract_data(self, query: str) -> dict:
        '''Extract the JSON data from the nominatim api using the input and return the data as a dictionary.'''
        full_url = BASE_NOMINATIM_URL + '/search?' + urllib.parse.urlencode([('q', query), ('format', 'json')])
        
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
        return json.loads(json_text)[0]
   

class ForwardGeocodeNominatimFile():
    '''Class used when the input for the center is through a file.'''
    def extract_data(self, path: str) -> dict:
        '''Extract the JSON data from the files provided using the input and return the data as a dictionary.'''
        f = None
        try:
            f = open(path, 'r')
            contents = f.read()
            f.close()
            data = json.loads(contents)[0]
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


def parse_center(center: str) -> tuple:
    '''Parse the given input string to decide to make a an API or File Nominatim object.'''
    if 'NOMINATIM' in center:
        user_input = center.split(' ', 2)[-1]
        nominatim_center = ForwardGeocodeNominatimAPI()
    elif 'FILE' in center:
        user_input = center.split(' ', 2)[-1]
        nominatim_center = ForwardGeocodeNominatimFile()

    dict_results = nominatim_center.extract_data(user_input)
    return (dict_results['lat'], dict_results['lon'])

    
