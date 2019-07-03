from service import weather_service


def weather_by_geolocation(id, lat, lon):
    if id == '1':
        return weather_service.current_by_geolocation(lat, lon)
    elif id == '2' or id == '3':
        return weather_service.detailed_by_geolocation(lat, lon)


def weather_by_city_name(id, name):
    if id == '1':
        return weather_service.current_by_city_name(name)
    elif id == '2' or id == '3':
        return weather_service.detailed_by_city_name(name)
    else:
        return None


def is_city_correct(name):
    return '404' != weather_service.current_by_city_name(name)['cod']
