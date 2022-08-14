from pathlib import Path
import json
import urllib.parse
import urllib.request
import urllib.error
import math
import time

class ReverseGeoFile:
    def __init__(self, p: str, data_list: list[dict]):
        self._paths = []
        list_of_paths = p.split()
        for x in list_of_paths:
            try:
                self._paths.append(json.loads(self._read_file(Path(x))))
            except json.JSONDecodeError:
                print('FAILED')
                print(x)
                print('FORMAT')
                exit()

    def _read_file(self, file: Path):
        try:
            the_file = open(file)
            file_content = the_file.read()
            the_file.close()
        except FileNotFoundError:
            print('FAILED')
            print(file)
            print('MISSING')
            exit()
        else:
            return file_content

    def get_reverse_data(self):
        reverse_locations = []
        for x in self._paths:
            reverse_locations.append(x['display_name'])
        return reverse_locations



