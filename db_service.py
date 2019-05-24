import pymongo

CLUSTER_URL = 'mongodb+srv://anrix:uh28IkToDvmTd2aG@cluster0-xqrtl.mongodb.net/admin'
DB_NAME = 'all_data'
COLLECTION_NAME = 'users'

client = pymongo.MongoClient(CLUSTER_URL)
users = client[DB_NAME][COLLECTION_NAME]

users_cities = {}

USER_ID_KEY = 'user_id'
CITY_KEY = 'city'
TIME_KEY = 'time'


def init():
    for u in users.find({}):
        users_cities[u[USER_ID_KEY]] = u[CITY_KEY]


def add_city(user_id, city):
    if user_id not in users_cities:
        users.insert({USER_ID_KEY: user_id, CITY_KEY: city, TIME_KEY: '_none_'})
    else:
        users.find_one_and_update({USER_ID_KEY: user_id}, {"$set": {CITY_KEY: city}});

    users_cities[user_id] = city
