import requests

OPEN_WEATHER_API_KEY = '440fe8d0120f53d0f7e381a3e91201b5'

BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'

WEATHER_LAT_PARAM = 'lat='
WEATHER_LON_PARAM = '&lon='

WEATHER_CITY_PARAM = 'q='

WEATHER_CELSIUS_PARAM = '&units=metric'

APP_ID_URL = '&appid='


def get_weather_by_geo(lat, lon):
    url = BASE_URL + WEATHER_LAT_PARAM \
          + lat + WEATHER_LON_PARAM + lon \
          + APP_ID_URL + OPEN_WEATHER_API_KEY + WEATHER_CELSIUS_PARAM

    return requests.get(url).json()


def get_weather_by_city_name(name):
    url = BASE_URL + WEATHER_CITY_PARAM + name \
          + APP_ID_URL + OPEN_WEATHER_API_KEY + WEATHER_CELSIUS_PARAM

    return requests.get(url).json()
