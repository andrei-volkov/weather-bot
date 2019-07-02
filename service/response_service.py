from service import weather_service


def get_by_query_geo(id, lat, lon):
    if id == '1':
        return weather_service.current_weather_by_geo(lat, lon)
    elif id == '2' or id == '3':
        return weather_service.detailed_weather_by_geo(lat, lon)


def get_by_query_name(id, name):
    if id == '1':
        return weather_service.current_weather_by_city_name(name)
    elif id == '2' or id == '3':
        return weather_service.detailed_weather_by_city_name(name)
    else:
        return None


def is_city_correct(name):
    return '404' != weather_service.current_weather_by_city_name(name)['cod']
