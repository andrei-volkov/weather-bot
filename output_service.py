thunderstorm = u'\U0001F4A8'  # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'  # Code: 300's
rain = u'\U00002614'  # Code: 500's
snowflake = u'\U00002744'  # Code: 600's snowflake
snowman = u'\U000026C4'  # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'  # Code: 700's foogy
clearSky = u'\U00002600'  # Code: 800 clear sky
fewClouds = u'\U000026C5'  # Code: 801 sun behind clouds
clouds = u'\U00002601'  # Code: 802-803-804 clouds general
hot = u'\U0001F525'  # Code: 904
default_emoji = u'\U0001F300'  # default emojis
wind = '💨'


def current_weather(response):
    weather_id = response['weather'][0]['id']

    return 'Current temperature: ' + str(response['main']['temp']) + '°C' \
           + '\nWeather: ' + response['weather'][0]['description'] + get_emoji(weather_id) \
           + '\nExpected temperature: ' \
           + str(response['main']['temp_min']) + ' - ' + str(response['main']['temp_max']) \
           + '\nAtmosphere pressure: ' + str(response['main']['pressure']) \
           + '\nWind speed: ' + str(response['wind']['speed']) + 'm/s' + wind


def detailed_weather(response):
    current_date = None
    result = ''

    for time_point in response['list']:
        if current_date is None:
            current_date = time_point['dt_txt'].split(' ')[0]

            result += 'Weather forecast for: *' + current_date + '* \n\n'
        elif current_date not in time_point['dt_txt']:
            break

        weather_id = time_point['weather'][0]['id']

        result += 'Time: ' + time_point['dt_txt'].split(' ')[1]
        result += '\nWeather: ' + time_point['weather'][0]['description'] + get_emoji(weather_id)
        result += '\nCurrent temperature: ' + str(time_point['main']['temp']) + '°C'
        result += '\nWind speed: ' + str(time_point['wind']['speed']) + 'm/s' + wind + '\n\n'

    return result


def output_by_id(id, response):
    if id == '1':
        return current_weather(response)
    elif id == '2':
        return detailed_weather(response)


def get_emoji(weather_id):
    if weather_id:
        if str(weather_id)[0] == '2' or weather_id == 900 or \
                weather_id == 901 or weather_id == 902 or weather_id == 905:
            return thunderstorm
        elif str(weather_id)[0] == '3':
            return drizzle
        elif str(weather_id)[0] == '5':
            return rain
        elif str(weather_id)[0] == '6' or weather_id == 903 or weather_id == 906:
            return snowflake + ' ' + snowman
        elif str(weather_id)[0] == '7':
            return atmosphere
        elif weather_id == 800:
            return clearSky
        elif weather_id == 801:
            return fewClouds
        elif weather_id == 802 or weather_id == 803 or weather_id == 803:
            return clouds
        elif weather_id == 904:
            return hot
        else:
            return default_emoji  # Default emoji

    else:
        return default_emoji  # Default emoji
