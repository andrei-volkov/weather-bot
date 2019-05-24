import requests
import schedule

import db_service
import main
import output_service
import response_service

alerts = {}
BASE_URL = 'https://api.telegram.org/bot' + main.TOKEN + \
           '/sendMessage?'


def add_alert(time, chat_id):
    if time != '_none_':
        if chat_id in alerts:
            remove_alert(chat_id)

        schedule.every().day.at(time).do(send_alert, chat_id).tag(chat_id)
        alerts[chat_id] = time
        db_service.add_alert(chat_id, time)


def remove_alert(chat_id):
    db_service.add_alert(chat_id, '_none_')
    schedule.clear(chat_id)
    del alerts[chat_id]


def send_alert(chat_id):
    response = response_service.get_by_query_name('1', db_service.users_cities[chat_id])
    res = output_service.output_by_id('1', response)

    url = BASE_URL + 'chat_id=' + str(chat_id) + '&text=' + res
    requests.post(url)
