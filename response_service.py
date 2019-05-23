import weather_service


def get_by_query_id(id, lat, lon):
    if id == '1':
        return weather_service.current_weather_by_geo(lat, lon)
    elif id == '2':
        return weather_service.detailed_weather_by_geo(lat, lon)


def get_by_query_id(id, name):
    if id == '1':
        return weather_service.current_weather_by_city_name(name)
    elif id == '2':
        return weather_service.detailed_weather_by_city_name(name)