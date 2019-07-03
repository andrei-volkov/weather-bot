import requests

openweathermap_api_key = 'api_key'

base_url = 'http://api.openweathermap.org/data/2.5/'

city_name_param, lat_param, lon_param = 'q=', 'lat=', '&lon='
current_param, detailed_param = 'weather?', 'forecast?'

celsius_param = '&units=metric'
app_id_param = '&appid='


def current_by_geolocation(lat, lon):
    url = base_url + current_param \
          + lat_param + lat \
          + lon_param + lon \
          + app_id_param + openweathermap_api_key + celsius_param

    return requests.get(url).json()


def current_by_city_name(name):
    url = base_url + current_param + \
          city_name_param + name \
          + app_id_param + openweathermap_api_key + celsius_param

    return requests.get(url).json()


def detailed_by_geolocation(lat, lon):
    url = base_url + detailed_param \
          + lat_param + lat \
          + lon_param + lon \
          + app_id_param + openweathermap_api_key + celsius_param

    return requests.get(url).json()


def detailed_by_city_name(name):
    url = base_url + detailed_param + \
          city_name_param + name \
          + app_id_param + openweathermap_api_key + celsius_param

    return requests.get(url).json()
