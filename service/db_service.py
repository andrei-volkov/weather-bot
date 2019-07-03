import pymongo

from service import alert_service

cluster = 'cluster_url'

name, collection = 'database_name', 'collection_name'

client = pymongo.MongoClient(cluster)
users = client[name][collection]
cities = {}

user_id_key, city_key, time_key = 'user_id', 'city', 'time'


def init():
    for u in users.find({}):
        cities[u[user_id_key]] = u[city_key]

        alert_service.add_alert(u[time_key], u[user_id_key])


def add_city(user_id, city):
    if user_id not in cities:
        users.insert({user_id_key: user_id, city_key: city, time_key: '_none_'})
    else:
        users.find_one_and_update({user_id_key: user_id}, {"$set": {city_key: city}})

    cities[user_id] = city


def add_alert(user_id, time):
    users.find_one_and_update({user_id_key: user_id}, {"$set": {time_key: time}})
