from pathlib import Path
import json
import urllib.parse
import urllib.request
import urllib.error
import math

class ForwardGeoFile:
    def __init__(self, file: Path):
        the_file = self._read_file(Path(file))
        try:
            self._nominatim_file = (json.loads(the_file))[0]
        except json.JSONDecodeError:
            print('FAILED')
            print(file)
            print('FORMAT')
            exit()
        else:
            self._lat = float(self._nominatim_file['lat'])
            self._lon = float(self._nominatim_file['lon'])
            self._name = self._nominatim_file['display_name']

    def get_forward_geo(self):
        return ({'lat': self._lat, 'lon': self._lon, 'name': self._name})

    def _read_file(self, file: Path):
        try:
            the_file = open(Path(file))
            file_content = the_file.read()
            the_file.close()
            
        except FileNotFoundError:
            print('FAILED')
            print(file)
            print('MISSING')
            exit()
            
        else:
            return file_content
