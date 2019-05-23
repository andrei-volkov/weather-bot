import requests

OPEN_WEATHER_API_KEY = '440fe8d0120f53d0f7e381a3e91201b5'

BASE_URL = 'http://api.openweathermap.org/data/2.5/'

WEATHER_LAT_PARAM = 'lat='
WEATHER_LON_PARAM = '&lon='

WEATHER_CURRENT = 'weather?'
WEATHER_DETAILED = 'forecast?'

WEATHER_CITY_PARAM = 'q='

WEATHER_CELSIUS_PARAM = '&units=metric'

APP_ID_URL = '&appid='


def current_weather_by_geo(lat, lon):
    url = BASE_URL + WEATHER_CURRENT \
          + WEATHER_LAT_PARAM + lat \
          + WEATHER_LON_PARAM + lon \
          + APP_ID_URL + OPEN_WEATHER_API_KEY + WEATHER_CELSIUS_PARAM

    return requests.get(url).json()


def current_weather_by_city_name(name):
    url = BASE_URL + WEATHER_CURRENT + \
          WEATHER_CITY_PARAM + name \
          + APP_ID_URL + OPEN_WEATHER_API_KEY + WEATHER_CELSIUS_PARAM

    return requests.get(url).json()


def detailed_weather_by_geo(lat, lon):
    url = BASE_URL + WEATHER_DETAILED \
          + WEATHER_LAT_PARAM + lat \
          + WEATHER_LON_PARAM + lon \
          + APP_ID_URL + OPEN_WEATHER_API_KEY + WEATHER_CELSIUS_PARAM

    return requests.get(url).json()


def detailed_weather_by_city_name(name):
    url = BASE_URL + WEATHER_DETAILED + \
          WEATHER_CITY_PARAM + name \
          + APP_ID_URL + OPEN_WEATHER_API_KEY + WEATHER_CELSIUS_PARAM

    return requests.get(url).json()
