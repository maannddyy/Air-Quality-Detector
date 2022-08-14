from pathlib import Path
import json
import urllib.parse
import urllib.request
import urllib.error
import math
import time

class AirQualityAPI:
    def __init__(self, radius: int, threshold: int, max_searches: int, center_lat: float, center_lon: float):
        self._threshold = threshold
        self._radius = radius
        self._max = max_searches
        self._center_lat = center_lat
        self._center_lon = center_lon
        self._air_qualities = self._open_url('https://www.purpleair.com/data.json')
        
    def get_aqi_data(self):
        locations = self._locations_of_interest()
        data = []
        for location in locations:
            data.append({'name': location[26], 'lat': location[27], 'lon': location[28], 'aqi': self._aqi(location[1])})
        return data

    def _locations_of_interest(self):
        locations = []
        for location in self._air_qualities['data']:
            if 0 <= self._distance(self._center_lat, self._center_lon, location[27], location[28]) <= self._radius:
                if (location[4] <= 3600):
                    if (location[25] == 0):
                        if (self._aqi(location[1]) > self._threshold):
                            locations.append(location)
        if len(locations) > self._max:
            locations = self._determine_max(locations)
        return locations

    def _open_url(self, url: str):
        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            data = response.read()
            response.close()
            
        except urllib.error.HTTPError as e:
            print('FAILED')
            print(f'{e.code} {url}')
            print('NOT 200')
            exit()

        except urllib.error.URLError:
            print('FAILED')
            print(url)
            print('NETWORK')
            exit()

        else:
            try:
                parse = data.decode(encoding = 'utf-8')
                parsed_json = json.loads(parse)
                
            except JSONDecodeError:
                print('FAILED')
                print('200 https://www.purpleair.com/data.json')
                print('FORMAT')
                exit()

            else:
                return parsed_json
            
    
    def _distance(self, lat1: float, lon1: float, lat2: float, lon2: float):
        if (lat2 == None or lon2 == None):
            return -1
        dlon = math.radians(lon2 - lon1)
        dlat = math.radians(lat2 - lat1)
        alat = math.radians((lat2 + lat1) / 2)
        x = (dlon) * math.cos(alat)
        return math.sqrt((x**2) + (dlat**2)) * 3958.8
    
    def _aqi(self, concentration: float):
        aqi = 0
        if 0 <= concentration < 12.1:
            return round((concentration / 12) * 50)
        elif 12.1 <= concentration < 35.5:
            return round(((concentration - 12.1) / (35.4 - 12.1)) * 49 + 51)
        elif 35.5 <= concentration < 55.5:
            return round(((concentration - 35.5) / (55.4 - 35.5)) * 49 + 101)
        elif 55.5 <= concentration < 150.5:
            return round(((concentration - 55.5) / (150.4 - 55.5)) * 49 + 151)
        elif 150.5 <= concentration < 250.5:
            return round(((concentration - 150.5) / (250.4 - 150.5)) * 99 + 201)
        elif 250.5 <= concentration < 350.5:
            return round(((concentration - 250.5) / (350.4 - 250.5)) * 99 + 301)
        elif 350.5 <= concentration < 500.5:
            return round(((concentration - 350.5) / (500.4 - 350.5)) * 99 + 401)
        elif concentration >= 500.5:
            return 501
        
    def _determine_max(self, places: list):
        locations = places[:self._max]
        new_locations = []
        
        for x in places[self._max:]:
            largest_values = []
            for element in locations:
                largest_values.append(element[1])
            if x[1] > min(largest_values):
                locations.append(x)
                i = largest_values.index(min(largest_values))
                locations.remove(locations[i])

        pm_values = []
        for x in locations:
            pm_values.append(x[1])
        pm_values.sort()
        
        for value in range(self._max - 1, -1, -1):
            for location in locations:
                if location[1] == pm_values[value]:
                    new_locations.append(location)
                    locations.remove(location)
        return new_locations

