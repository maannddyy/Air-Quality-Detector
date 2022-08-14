from pathlib import Path
import json
import urllib.parse
import urllib.request
import urllib.error
import math

class ForwardGeoAPI:
    def __init__(self, location: str):
        url = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode([('q', location), ('format', 'json')])
        self._nominatim_data = (self._open_url(url))[0]
        self._lat = self._nominatim_data['lat']
        self._lon = self._nominatim_data['lon']
        self._name = self._nominatim_data['display_name']

    def get_forward_geo(self):
        return ({'lat': self._lat, 'lon': self._lon, 'name': self._name})
        
    def _open_url(self, url: str):
        try:
            request = urllib.request.Request(url, headers = {'Referer': 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/mandyf'})
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
                print(f'200 {url}')
                print('FORMAT')
                exit()

            else:
                return parsed_json


