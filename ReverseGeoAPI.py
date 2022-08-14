from pathlib import Path
import json
import urllib.parse
import urllib.request
import urllib.error
import math
import time


class ReverseGeoAPI:
    def __init__(self, data_list: list[dict]):
        self._urls = []
        self._coordinates = []
        self._data_list = []
        for x in data_list:
            url = 'https://nominatim.openstreetmap.org/reverse?' + urllib.parse.urlencode([('lat', str(x['lat'])), ('lon', str(x['lon'])), ('format', 'json')])
            self._data_list.append(self._open_url(url))
            time.sleep(1)


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


    def get_reverse_data(self):
        reverse_locations = []
        for x in self._data_list:
            reverse_locations.append(x['display_name'])
        return reverse_locations


