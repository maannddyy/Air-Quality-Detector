from pathlib import Path
import json
import urllib.parse
import urllib.request
import urllib.error
import math
from ForwardGeoFile import ForwardGeoFile
from ForwardGeoAPI import ForwardGeoAPI
from AirQualityFile import AirQualityFile
from AirQualityAPI import AirQualityAPI
from ReverseGeoFile import ReverseGeoFile
from ReverseGeoAPI import ReverseGeoAPI

def forward_geocoding() -> dict:
    line_1 = input()
    if line_1[:17] == 'CENTER NOMINATIM ':
        forward_geo = ForwardGeoAPI(line_1[17:])
    elif line_1[:12] == 'CENTER FILE ':
        forward_geo = ForwardGeoFile(line_1[12:])
        
    center_data = forward_geo.get_forward_geo()
    return center_data

def air_quality_list(center_info: dict) -> list[dict]:

    line_2 = input()
    if line_2[:6] == 'RANGE ':
        rad = int(line_2[6:])

    line_3  = input()
    if line_3[:10] == 'THRESHOLD ':
        threshold = int(line_3[10:])

    line_4 = input()
    if line_4[:4] == 'MAX ':
        max_searches = int(line_4[4:])

    line_5 = input()
    if line_5 == 'AQI PURPLEAIR':
        aqi_data = AirQualityAPI(rad, threshold, max_searches, float(center_info['lat']), float(center_info['lon']))
        
    elif line_5[:9] == 'AQI FILE ':
        aqi_data = AirQualityFile(line_5[9:], rad, threshold, max_searches, float(center_info['lat']), float(center_info['lon']))

    aqi_list = aqi_data.get_aqi_data()
    return aqi_list

def reverse_geocoding(aqi_info: list[dict]) -> list[str]:
    line_6 = input()
    if line_6 == 'REVERSE NOMINATIM':
        reverse_geo = ReverseGeoAPI(aqi_info)
    elif line_6[:14] == 'REVERSE FILES ':
        reverse_geo = ReverseGeoFile(line_6[14:], aqi_info)

    reverse_data = reverse_geo.get_reverse_data()
    return reverse_data

def _convert(x: float, y: float):
    lat = ''
    if x < 0:
        lat = str(abs(x)) + '/S'
    else:
        lat = str(x) + '/N'

    lon = ''
    if y < 0:
        lon = str(abs(y)) + '/W'
    else:
        lon = str(y) + '/E'

    return lat + ' ' + lon

def print_output(center_data: dict, aqi_data: list[dict], reverse_data: list[str]) -> None:
    print('CENTER ' + _convert(float(center_data['lat']), float(center_data['lon'])))
    count = 0
    for loc in aqi_data:
        print('AQI ' + str(loc['aqi']))
        print(_convert(float(loc['lat']), float(loc['lon'])))
        print(reverse_data[count])
        count += 1
          

def run():
    center = forward_geocoding()
    list_of_aqi = air_quality_list(center)
    reverse_locations = reverse_geocoding(list_of_aqi)
    print_output(center, list_of_aqi, reverse_locations)

if __name__ == '__main__':
    run()

